# 24 · Python interview Q&A

1. **Mutable vs immutable?** list/dict/set vs int/str/tuple/frozenset. Never use a mutable default argument (`def f(x=[])`); use `None`.
2. **`is` vs `==`?** Identity vs equality.
3. **`*args`, `**kwargs`?** Extra positional / keyword arguments; also unpack when calling.
4. **List vs tuple vs set vs dict?** Ordered mutable / ordered immutable / unique unordered / key → value (insertion ordered since 3.7).
5. **Shallow vs deep copy?** `copy.copy` copies the container; `copy.deepcopy` copies nested objects.
6. **What is the GIL?** A lock letting one thread run Python bytecode at a time; threads help I/O, not CPU. ([21](21_concurrency_and_asyncio.md))
7. **Generator vs list?** Lazy single-pass vs all in memory. ([19](19_iterators_and_generators.md))
8. **Decorator?** A callable wrapping another callable. ([23](23_decorators_and_context_managers.md))
9. **`__new__` vs `__init__`?** Creates the instance vs initialises it.
10. **MRO?** C3 linearisation order for method lookup; `Class.__mro__`; `super()` follows it. ([03](03_inheritance.md))
11. **`@staticmethod` vs `@classmethod`?** No implicit arg vs receives the class (alternate constructors).
12. **`__str__` vs `__repr__`?** Human-readable vs unambiguous/debug.
13. **Dunder methods?** `__len__`, `__eq__`, `__hash__`, `__iter__`, `__enter__`... they make objects work with built-ins.
14. **dataclass vs NamedTuple vs pydantic?** Plain typed class / immutable tuple / runtime validation. ([07](07_dataclasses_and_typing.md))
15. **ABC vs Protocol?** Nominal (must inherit) vs structural. ([05](05_abstraction.md))
16. **How does memory management work?** Reference counting + cyclic garbage collector.
17. **Exceptions best practice?** Catch specific exceptions, custom hierarchy, `raise ... from err`, `finally`/`with` for cleanup. ([08](08_exceptions.md))
18. **`match` statement?** Structural pattern matching (3.10+) on shapes, classes, literals.
19. **Comprehensions vs `map`/`filter`?** Comprehensions are usually clearer; both are lazy only as generator expressions/iterators. ([17](17_functional_programming.md))
20. **Closures?** Inner function capturing outer variables; `nonlocal` to rebind.
21. **async vs threads?** Cooperative single-thread I/O vs OS threads.
22. **How do you package/ship code?** `pyproject.toml`, lock file, wheel; venvs per project. ([22](22_virtual_envs_and_packaging.md))
23. **How do you test?** pytest, fixtures, parametrize, mocks at boundaries, coverage. ([11](11_testing_with_pytest.md))
24. **What's new recently?** 3.11 speed + `TaskGroup` + `ExceptionGroup`; 3.12 PEP 695 generics + f-string grammar; 3.13 new REPL, experimental free-threading and JIT; 3.14 template strings (t-strings), deferred annotations.
