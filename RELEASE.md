# Release Checklist

Before publishing `hitl-work.skill`:

1. Ensure all agent documents listed in `SKILL.md` exist at repository root.
2. Rebuild the archive from the repository parent directory:

   ```sh
   rm -f hitl-work/hitl-work.skill
   zip -qr hitl-work/hitl-work.skill hitl-work \
     -x 'hitl-work/.git/*' 'hitl-work/hitl-work.skill' 'hitl-work/tools/*' 'hitl-work/RELEASE.md'
   ```

3. Validate the package:

   ```sh
   python3 hitl-work/tools/validate-release.py
   ```

4. Inspect the final diff and archive listing before publishing.

The validator checks that every agent file referenced by `SKILL.md` or `README.md` exists in both source and `hitl-work.skill`.
