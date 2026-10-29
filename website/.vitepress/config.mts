import { defineConfig } from 'vitepress';
import { withMermaid } from 'vitepress-plugin-mermaid';
import side from './sidebar.generated.json' with { type: 'json' };

const GH = 'https://github.com/junaaid96/python-oop-cli-projects';
const SITE = 'https://junaaid96.github.io/python-oop-cli-projects/';

export default withMermaid(defineConfig({
  srcDir: 'content',
  base: '/python-oop-cli-projects/',
  lang: 'en-US',
  title: 'Python OOP CLI Projects',
  titleTemplate: ':title · Python OOP CLI Projects',
  description: 'Learn object-oriented Python 3.13 through 15 laddered CLI projects and a Django + DRF capstone, with concept guides, tests and exercises.',
  cleanUrls: true,
  lastUpdated: true,
  sitemap: { hostname: SITE },
  head: [
    ['meta', { name: 'theme-color', content: '#3572a5' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'Python OOP CLI Projects' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
  ],
  transformPageData(page) {
    const route = page.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '');
    const title = page.frontmatter.title || page.title || 'Python OOP CLI Projects';
    const desc = page.frontmatter.description || page.description || '';
    page.frontmatter.head ??= [];
    page.frontmatter.head.push(
      ['link', { rel: 'canonical', href: SITE + route }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:url', content: SITE + route }],
      ['meta', { property: 'og:description', content: desc }],
    );
  },
  markdown: {
    lineNumbers: true,
    config(md) {
      // Template syntax such as {{ value }} in inline code must not be compiled by Vue.
      const orig = md.renderer.rules.code_inline!;
      md.renderer.rules.code_inline = (...args) => orig(...args).replace('<code', '<code v-pre');
    },
  },
  themeConfig: {
    nav: [
      { text: 'Learning path', link: '/guides/00-learning-path' },
      { text: 'Guides', link: '/guides/01-classes-and-objects' },
      { text: 'Django & DRF', link: '/django/' },
      { text: 'Projects', link: '/projects/01-contact-book' },
    ],
    sidebar: [
      { text: 'Learning path', items: [{ text: 'Overview', link: '/' }, ...side.path] },
      { text: 'Core OOP guides (01-18)', collapsed: false, items: side.core },
      { text: 'Advanced Python (19-24)', collapsed: false, items: side.advanced },
      { text: 'Django & DRF track (D01-D15)', collapsed: true, items: side.django },
      { text: 'Projects (01-16)', collapsed: false, items: side.projects },
    ],
    socialLinks: [{ icon: 'github', link: GH }],
    search: { provider: 'local' },
    outline: { level: [2, 3] },
    editLink: {
      pattern: ({ frontmatter }) => `https://github.com/junaaid96/python-oop-cli-projects/blob/main/${frontmatter.source ?? ''}`,
      text: 'View source on GitHub',
    },
    footer: { message: 'Released under the MIT License.', copyright: '© 2026 Md. Junaidul Islam' },
  },
  mermaid: { theme: 'default' },
}));
