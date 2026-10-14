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

---

## GitHub Release Flow

1. Update `CHANGELOG.md`: move items from `[Unreleased]` into a new version section with today's date.
2. Commit the changelog on `main`.
3. Tag and push the release:

   ```sh
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. On GitHub, create a Release from the tag and paste the changelog section as the release notes.

Use semantic versioning: MAJOR for breaking workflow changes, MINOR for new agents or stages, PATCH for prompt fixes and clarifications.
