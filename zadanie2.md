# Opis etapów
1. Inicjalizacja środowiska: pobranie kodu źródłowego (`actions/checkout`), konfiguracja emulatora `QEMU` (w celu wsparcia dla architektury ARM64) oraz uruchomienie `Docker Buildx`.
2. Uwierzytelnianie: logowanie do GHCR  za pomocą automatycznego tokenu `${{ secrets.GITHUB_TOKEN }}` oraz do rejestru DockerHub z wykorzystaniem sekretów repozytorium (`DOCKERHUB_USERNAME` i `DOCKERHUB_TOKEN`).
3. Ekstrakcja metadanych: automatyczne generowanie tagów i etykiet OCI na podstawie stanu repozytorium Git.
4. Lokalne budowanie testowe: skompilowanie obrazu dla architektury maszynowej runnera (`linux/amd64`) i załadowanie go (`load: true`).
5. Skan Trivy: przeskanowanie lokalnego obrazu za pomocą narzędzia Trivy. Jeśli zostaną wykryte podatności o statusie `HIGH` lub `CRITICAL`, zwaracany jest kod błędu `exit-code: '1'`, co natychmiast przerywa działanie potoku i blokuje dystrybucję obrazu.
6. Budowanie docelowe i dystrybucja: równoległe zbudowanie obrazu dla architektur `linux/amd64` oraz `linux/arm64` i jednoczesne wysłanie (`push: true`) gotowego artefaktu na GHCR oraz aktualizacja zewnętrznej pamięci podręcznej (cache) na DockerHub.
---
# Tagowanie

### tagowanie obrazu aplikacji (GHCR)
Wykorzystano dynamiczne generowanie tagów za pomocą akcji `docker/metadata-action`:
* `latest` – przypisywany automatycznie tylko dla najświeższych zmian scalonych z główną gałęzią (`main`/`master`).
* Skrócony hash commitu (SHA) – unikalny, niezmienny (immutable) identyfikator generowany przy każdym uruchomieniu potoku, zapewniający pełną identyfikowalność (*traceability*) kodu.
* Wersjonowanie semantyczne (`v*.*.*`) – wyzwalane automatycznie w momencie opublikowania oficjalnego tagu wersji w systemie Git (np. `v1.0.0`).

Uzasadnienie: 
Zgodnie z dobrym praktykami projektowania aplikacji chmurowych, poleganie wyłącznie na tagu `latest` w środowiskach produkcyjnych jest antywzorcem. Stałe wiązanie obrazów z hashem SHA gwarantuje powtarzalność wdrożeń i eliminuje błędy typu *race conditions* podczas skalowania środowisk kontenerowych.

### oznaczenie danych cache (DockerHub)
Dane pamięci podręcznej są kierowane do dedykowanego, publicznego repozytorium na DockerHub z jawnym tagiem `:cache`, wykorzystując backend typu `registry` w trybie `mode=max`.

---
# ustawienie secretów

```
D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh secret set DOCKERHUB_USERNAME
? Paste your secret: **********
✓ Set Actions secret DOCKERHUB_USERNAME for KamilRodak/Zadanie2

D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh secret set DOCKERHUB_TOKEN
? Paste your secret: ************************************
✓ Set Actions secret DOCKERHUB_TOKEN for KamilRodak/Zadanie2
```
---

# testy GHActions

### poprawne działanie
```
D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh workflow run
? Select a workflow Zadanie 2 - CI/CD (gha_zad2.yml)
✓ Created workflow_dispatch event for gha_zad2.yml at main
https://github.com/KamilRodak/Zadanie2/actions/runs/26692603964

To see the created workflow run, try: gh run view 26692603964
To see runs for this workflow, try: gh run list --workflow="gha_zad2.yml"

D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh run watch
? Select a workflow run * Zadanie 2 - CI/CD, Zadanie 2 - CI/CD [main] 3s ago
✓ main Zadanie 2 - CI/CD · 26692603964
Triggered via workflow_dispatch about 1 minute ago

JOBS
✓ build-and-secure in 1m51s (ID 78671589628)
  ✓ Set up job
  ✓ Checkout repo
  ✓ QEMU Set up
  ✓ Buildx Set up
  ✓ Zaloguj do ghcr.io
  ✓ Zaloguj do Dockerhuba
  ✓ Extract Docker metadata for GHCR
  ✓ Zbuduj lokalnie obraz do skanu
  ✓ Skanowanie obrazu Trivy
  - Jesli wykryto bledy, wyswietl informacje i przerwij
  ✓ Zbuduj i wypchnij GHCR
  ✓ Post Zbuduj i wypchnij GHCR
  ✓ Post Skanowanie obrazu Trivy
  ✓ Post Zbuduj lokalnie obraz do skanu
  ✓ Post Zaloguj do Dockerhuba
  ✓ Post Zaloguj do ghcr.io
  ✓ Post Buildx Set up
  ✓ Post QEMU Set up
  ✓ Post Checkout repo
  ✓ Complete job

ANNOTATIONS
! Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, docker/build-push-action@v6, docker/login-action@v3, docker/metadata-action@v5, docker/setup-buildx-action@v3, docker/setup-qemu-action@v3. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
build-and-secure: .github#2


✓ Run Zadanie 2 - CI/CD (26692603964) completed with 'success'

D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>
```

### wystąpenie błędów HIGH lub CRITICAL
```
D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh workflow run
? Select a workflow Zadanie 2 - CI/CD (gha_zad2.yml)
✓ Created workflow_dispatch event for gha_zad2.yml at main
https://github.com/KamilRodak/Zadanie2/actions/runs/26693375332

To see the created workflow run, try: gh run view 26693375332
To see runs for this workflow, try: gh run list --workflow="gha_zad2.yml"

D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>gh run watch
? Select a workflow run * Zadanie 2 - CI/CD, Zadanie 2 - CI/CD [main] 2s ago
X main Zadanie 2 - CI/CD · 26693375332
Triggered via workflow_dispatch less than a minute ago

JOBS
X build-and-secure in 34s (ID 78673599984)
  ✓ Set up job
  ✓ Checkout repo
  ✓ QEMU Set up
  ✓ Buildx Set up
  ✓ Zaloguj do ghcr.io
  ✓ Zaloguj do Dockerhuba
  ✓ Ekstrakcja metadanych dla GHCR
  ✓ Zbuduj lokalnie obraz do skanu
  X Skanowanie obrazu Trivy
  X Jesli wykryto bledy, wyswietl informacje i przerwij
  - Zbuduj i wypchnij GHCR
  ✓ Post Skanowanie obrazu Trivy
  ✓ Post Zbuduj lokalnie obraz do skanu
  ✓ Post Zaloguj do Dockerhuba
  ✓ Post Zaloguj do ghcr.io
  ✓ Post Buildx Set up
  ✓ Post QEMU Set up
  ✓ Post Checkout repo
  ✓ Complete job

ANNOTATIONS
! Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/github-script@v7, docker/build-push-action@v6, docker/login-action@v3, docker/metadata-action@v5, docker/setup-buildx-action@v3, docker/setup-qemu-action@v3. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
build-and-secure: .github#2

X Wykryto podatnosci HIGH lub CRITICAL
build-and-secure: .github#44

X Process completed with exit code 1.
build-and-secure: .github#587


X Run Zadanie 2 - CI/CD (26693375332) completed with 'failure'
```

### własne otagowanie
```
D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>git tag v2.3.7

D:\Pliki\Pliki Studia\Programowanie_aplikacji_w_chmurze_obliczeniowej\Zadanie2>git push origin v2.3.7
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/KamilRodak/Zadanie2
 * [new tag]         v2.3.7 -> v2.3.7

```