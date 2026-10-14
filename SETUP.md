# Setup guide — Mosharof Hossain's Neon Circuit profile

This profile design is original and uses a neon-circuit visual identity (cyan + violet on a dark background). It is inspired by the general idea of an animated, detailed developer profile, not copied from another person's README.

## 1. Make your profile README

1. Open https://github.com/new
2. Repository name: `ShadinWorld` (it must match your CURRENT username exactly).
3. Set visibility to **Public**.
4. Turn **Add a README file** on.
5. Create the repository.
6. Upload the included `README.md` and the `assets` folder (which contains `neon-header.svg`) to the repository root. Replace the generated README if needed.

## 2. Turn on the contribution snake

1. In the `ShadinWorld` repository, open **Add file → Create new file**.
2. Enter this path as the filename: `.github/workflows/snake.yml`
3. Paste the included workflow file and commit it to the repository's default branch.
4. Open the repository's **Actions** tab. If prompted, enable Actions.
5. Choose **Generate contribution snake** → **Run workflow**.
6. After it completes successfully, a branch named `output` should appear. Reload the profile README; the snake image will then have a file to load.

If the workflow fails, check that Actions are enabled and that the repository's Actions settings permit workflows to write repository contents. Do not add a personal access token to the README.

## 3. Important checks before publishing

- Confirm each project description accurately matches the code in that repository.
- `ewu-studyhub-web` and `laptop-price-analysis` are linked using the repository names visible on your public profile.
- Add your LinkedIn link only if you have the exact public URL. No fake link is included.
- If you change your GitHub username later, update the username in all README image URLs and the snake workflow.

## 4. About the animated widgets

The typing animation, statistics cards, streak card, activity graph, and visitor counter are hosted by third-party services. Their availability and displayed numbers may vary; the widgets are decorative and are not official GitHub metrics. The contribution snake requires the GitHub Actions workflow above to generate the image.
