# TOOLS.md - Tool Configuration & Notes

> Document tool-specific configurations, gotchas, and credentials here.

## Credentials Location

All credentials stored in `.credentials/` (gitignored).

## Tool Notes

Add notes about tool configurations as needed.

### Next.js + Tailwind + Vercel Deployment

**Critical: tailwind.config.ts format**
- Must be TypeScript config object, NOT CSS with @tailwind directives
- Correct: `export default { content: [], theme: {}, plugins: [] }`
- Wrong: `@tailwind base; @tailwind components; @tailwind utilities;`

**CSS File Organization**
- `globals.css` should only contain: `@tailwind base; @tailwind components; @tailwind utilities;`
- Custom CSS variables go in tailwind.config.ts theme.extend
- Component-specific styles use Tailwind classes

**Hook/Component Separation**
- Files in `app/hooks/` should NOT return JSX
- Keep hooks (useTypewriter) separate from components (ParagraphTypewriter)
- Import hooks in components, not the other way around

**Vercel Build Debugging**
- "Unexpected token" in CSS = webpack loader misconfiguration
- Check tailwind.config.ts isn't accidentally CSS
- Ensure postcss.config.js is present

---

### Git Push Issues - Subdirectory Projects

**Problem:** Git push hangs/times out when trying to push a project subdirectory to a new GitHub repo.

**Root Cause:** The subdirectory may not have its own `.git` directory and is being tracked by a parent workspace repo instead.

**Solution:**
```bash
# 1. Check if .git exists in project directory
ls -la /path/to/project/.git

# 2. If missing, initialize fresh repo
cd /path/to/project
git init
git add -A
git commit -m "Initial commit"

# 3. Add remote and push
git remote add origin https://github.com/user/repo.git
git push -u origin master
```

**Verification:** Always check `git remote -v` and `git status` before pushing to ensure you're pushing the right repo.

---

*Add whatever helps you do your job. This is your cheat sheet.*
