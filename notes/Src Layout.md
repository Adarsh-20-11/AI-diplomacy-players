---
tags: [concept]
phase: 0
status: draft
score: 4
last_reviewed: 2026-11-01
---

# Src Layout

## What it is (my own words)
The naming convention for the main folder could be whatever, but inside the main/root folder, you need to have a src folder, inside which another folder needs to be there with the name, but here, hyphens and other special characters other than underscore are not allowed.

Need for src: Without the src, the import needle statement might pick up your working directory as your main folder instead the actual package folder, making a lot of tests fail

Also, imports need to either be absolute (entire path) or relative (with the . behind), having regular file imports won't work in libraries, only the cellotape functions that you have.

*(imported verbatim from the 2026-10-28 session)*

## Where it lives in needle
- needle-ai/src/needle/


## Tradeoff / why I chose this


## Related
- [[pyproject.toml]]

## Quiz myself
1. 
2. 
3. 

## Reviews (Claude)
### 2026-11-01, score 4/5
- Correct: the hyphen/underscore rule, the root folder name being free, and the reason for `src/` (the working directory can shadow the installed package).
- Wrong or missing: "making a lot of tests fail" is backwards. Without `src/`, tests pass locally because they import the folder, and then fail for users who install the package. Your reason for relative imports is also partly off: the real reason is that the package gets imported from other places (a user's project, tests, another working directory), so a bare `from exceptions import ...` only works by accident.
- Corrected version: with `src/`, you can only import what is actually installed, so a broken package shows up in your own tests instead of in your users' projects. Imports inside a package are absolute (`needle.llmapi.exceptions`) or relative (`.exceptions`), never bare.
