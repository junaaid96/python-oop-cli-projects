// Generates website/content/ from the repo Markdown (single source of truth).
// Never edit website/content by hand: it is wiped and rebuilt on every build.
// legacy/ is intentionally not published; links into it point at GitHub.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const OUT = path.resolve(ROOT, 'website/content');
const GH = 'https://github.com/junaaid96/python-oop-cli-projects';

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const read = (p) => fs.readFileSync(p, 'utf8');
const slug = (f) => f.replace(/\.md$/, '').replace(/_/g, '-');

// repo-relative source path -> site route
const pages = new Map();
const guides = fs.readdirSync(path.join(ROOT, 'docs')).filter((f) => /^\d\d_.*\.md$/.test(f)).sort();
for (const f of guides) pages.set(`docs/${f}`, `guides/${slug(f)}`);
const django = fs.readdirSync(path.join(ROOT, 'docs/django')).filter((f) => /^\d\d_.*\.md$/.test(f)).sort();
pages.set('docs/django/README.md', 'django/');
for (const f of django) pages.set(`docs/django/${f}`, `django/${slug(f)}`);
const projects = fs.readdirSync(path.join(ROOT, 'projects'))
  .filter((d) => /^\d\d_/.test(d) && fs.existsSync(path.join(ROOT, 'projects', d, 'README.md'))).sort();
for (const d of projects) pages.set(`projects/${d}/README.md`, `projects/${slug(d)}`);

function resolveLink(fromRel, href) {
  if (/^([a-z]+:|#|\/)/i.test(href)) return href;
  const [p, hash = ''] = href.split('#');
  const h = hash ? `#${hash}` : '';
  const target = path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), p)).replace(/\/$/, '');
  for (const cand of [target, `${target}/README.md`]) if (pages.has(cand)) return `/${pages.get(cand)}${h}`;
  if (target === 'README.md' || target === '.') return `/${h}`;
  const abs = path.join(ROOT, target);
  const kind = fs.existsSync(abs) && fs.statSync(abs).isDirectory() ? 'tree' : 'blob';
  return `${GH}/${kind}/main/${target}${h}`;
}

// Rewrite relative links outside fenced code blocks.
function rewrite(md, fromRel) {
  let inFence = false;
  return md.split('\n').map((line) => {
    if (/^\s*(```|~~~)/.test(line)) { inFence = !inFence; return line; }
    if (inFence) return line;
    return line.replace(/\]\(([^)\s]+)\)/g, (_, h) => `](${resolveLink(fromRel, h)})`);
  }).join('\n');
}

const fm = (o) => `---\n${Object.entries(o).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n')}\n---\n\n`;
const firstHeading = (md) => (md.match(/^#\s+(.+)$/m) || [, ''])[1].trim();
const plain = (s) => s.replace(/[*_`]/g, '').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/&amp;/g, '&');
const firstPara = (md) => {
  const para = md.split('\n\n').find((b) => b.trim() && !/^(#|\||```|!\[|-|>|\d+\.)/.test(b.trim()));
  return plain((para || '').replace(/\s+/g, ' ').trim()).slice(0, 180);
};

// Main (non-test) modules of a project, embedded in collapsible blocks.
function walkPy(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name)).flatMap((e) => {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) return ['tests', 'migrations', '__pycache__'].includes(e.name) ? [] : walkPy(p);
    return e.name.endsWith('.py') && e.name !== '__init__.py' ? [p] : [];
  });
}
function sourceSection(dir) {
  const files = walkPy(path.join(ROOT, 'projects', dir));
  if (!files.length) return '';
  let s = `\n\n## Source code\n\nThe main modules of this project, embedded straight from the repo. Tests live in [tests/](${GH}/tree/main/projects/${dir}/tests); browse the whole folder on [GitHub](${GH}/tree/main/projects/${dir}).\n`;
  for (const f of files) {
    const r = rel(f);
    s += `\n::: details ${r.replace(`projects/${dir}/`, '')}\n[View on GitHub](${GH}/blob/main/${r})\n\n\`\`\`python\n${read(f).replace(/\n$/, '')}\n\`\`\`\n:::\n`;
  }
  return s;
}

function emit(route, srcRel, body, extra = {}) {
  const file = path.join(OUT, route.endsWith('/') ? `${route}index.md` : `${route}.md`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, fm({ source: srcRel, ...extra }) + body + '\n');
}

const side = { path: [], core: [], advanced: [], django: [], projects: [] };
for (const [srcRel, route] of pages) {
  const md = read(path.join(ROOT, srcRel));
  const title = plain(firstHeading(md));
  let body = rewrite(md, srcRel);
  const m = srcRel.match(/^projects\/([^/]+)\/README\.md$/);
  if (m) body += sourceSection(m[1]);
  emit(route, srcRel, body, { title: title.replace(/^(D?\d\d)\s*·\s*/, ''), description: firstPara(md) });
  const num = (srcRel.match(/(\d\d)_[^/]*$/) || [])[1];
  const item = { text: title.replace(/\s*·\s*/, '. ').replace(/\s*·.*$/, ''), link: `/${route}` };
  if (srcRel.startsWith('projects/')) side.projects.push(item);
  else if (srcRel.startsWith('docs/django/')) side.django.push(srcRel.endsWith('README.md') ? { text: 'Track overview', link: '/django/' } : { ...item, text: `D${item.text}` });
  else if (+num === 0) side.path.push({ text: 'Weekly learning path', link: `/${route}` });
  else (+num <= 18 ? side.core : side.advanced).push(item);
}

// Home page: hero + root README (minus title, badges and the Website section).
const readme = read(path.join(ROOT, 'README.md'));
const body = readme.split('\n').filter((l, i) => !(i === 0 && l.startsWith('# ')) && !/^\s*(\[!\[|!\[)/.test(l))
  .join('\n').replace(/^## Website[\s\S]*?(?=^## )/m, '').replace(/^- \[Website\]\(#website\)\n/m, '');
const home = fm({ layout: 'home', source: 'README.md', title: 'Python OOP CLI Projects', description: firstPara(body) })
  .replace(/---\n\n$/, `hero:
  name: "Python OOP CLI Projects"
  text: "Learn object-oriented Python by building 16 projects"
  tagline: "15 laddered CLI projects from a first class to layered, tested apps, plus a Django + DRF capstone. Every project has commented source, pytest tests and exercises."
  actions:
    - theme: brand
      text: Start the learning path
      link: /guides/00-learning-path
    - theme: alt
      text: First project
      link: /projects/01-contact-book
    - theme: alt
      text: View on GitHub
      link: ${GH}
features:
  - title: Core OOP (01-18)
    details: Classes, encapsulation, inheritance, polymorphism, ABC vs Protocol, SOLID, design patterns, clean code and functional style.
    link: /guides/01-classes-and-objects
  - title: Advanced Python (19-24)
    details: Generators, advanced typing, asyncio, packaging, decorators, context managers and interview Q&A.
    link: /guides/19-iterators-and-generators
  - title: Django & DRF (D01-D15)
    details: ORM, views, forms, auth, admin, REST APIs, caching, security, testing and deployment.
    link: /django/
  - title: 16 projects
    details: Contact Book to Text Adventure, then the FreelanceHub capstone, with source embedded on every page.
    link: /projects/01-contact-book
---

`);
fs.writeFileSync(path.join(OUT, 'index.md'), home + rewrite(body, 'README.md') + '\n');

fs.writeFileSync(path.resolve(ROOT, 'website/.vitepress/sidebar.generated.json'), JSON.stringify(side, null, 2));
console.log(`synced ${guides.length} guides, ${django.length} Django guides, ${projects.length} projects`);
