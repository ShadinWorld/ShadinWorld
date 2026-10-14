# Packet to Pixel — setup guide

This profile README uses an original teal / ultraviolet / amber circuit identity. It follows the *idea* of a detailed animated developer profile, but the layout, banner, wording, and content are tailored to Mosharof Hossain.

## Files in this package

- `README.md` — replace the contents of the profile repository's current README with this file.
- `assets/packet-to-pixel.svg` — custom banner used at the top of the README.
- `.github/workflows/snake.yml` — generates the contribution snake into the `output` branch.
- `.github/workflows/profile-3d.yml` — generates the 3D contribution calendar into `profile-3d-contrib/` on the default branch.

## Apply the design to the existing profile repository

1. Open `https://github.com/ShadinWorld/ShadinWorld`.
2. Upload/replace `README.md` and upload the `assets` folder containing `packet-to-pixel.svg`.
3. Add the workflow files using **Add file → Create new file**. Enter each exact path:
   - `.github/workflows/snake.yml`
   - `.github/workflows/profile-3d.yml`
   Copy the contents from this package's files and commit them.
4. Open the repository's **Actions** tab. If necessary, enable Actions and make sure the repository's workflow permissions allow workflows to write to the repository.
5. Run **Refresh 3D contribution calendar** once using **Run workflow**. When it succeeds, `profile-3d-contrib/profile-green-animate.svg` should appear in the repository.
6. Run **Generate contribution snake** once. When it succeeds, an `output` branch should contain `github-contribution-grid-snake-dark.svg`.
7. Reload `https://github.com/ShadinWorld` to verify the profile README. If a widget is blank immediately after setup, check that workflow has completed and try again later.

## Important

- This changes only the profile README and its supporting assets/workflows. It does not delete or rename your other repositories.
- Your profile README repository name must match your current username exactly: `ShadinWorld`. If the username changes later, update the username in the widget URLs and snake workflow.
- No personal access token needs to be created. The workflows use GitHub's automatically provided `GITHUB_TOKEN`.
- Third-party widgets (typing SVG, stats, streak, trophies, activity graph, visitor counter) may occasionally be rate-limited or unavailable. They are decorative profile elements, not official employment or skill certifications.
- Review all project descriptions and skill icons before committing. The wording is based on your CV and public repository descriptions, and it avoids claiming expert-level proficiency.
