# How to run dataset preprocessing and audio extraction

Run [01_data_preprocessing.ipynb](notebooks/01_data_preprocessing.ipynb), then
[02_audio_extraction.ipynb](notebooks/02_audio_extraction.ipynb). Both stages
run on CPU. They prepare the evaluation inputs; they do not train models or
calculate translation quality.

The notebooks currently use different environments: notebook 01 uses Google
Colab and Drive, while notebook 02 uses local Windows paths. The path changes
below are required for your own replay. This guide does not change the notebooks.

## Inputs and environment

Use the same Common Voice Scripted Speech 26.0 English release as the completed
experiment, together with the CoVoST 2 translation files. A fresh clone does
not include the source dataset or audio.

| Input | Used by | Required fields or contents |
|---|---|---|
| `validated.tsv` | Notebook 01 | `path`, `sentence_id`, `sentence`, `client_id`, `accents` |
| `clip_durations.tsv` | Notebook 01 | `clip`, `duration[ms]` |
| CoVoST 2 English-to-target TSV files | Notebook 01 | `path`, `translation`; downloaded by its Bash cell |
| Common Voice English `.tar.gz` archive | Notebook 02 | Audio files named in the sampled metadata's `path` column |

Notebook 01 compares German, Chinese, Japanese and Indonesian reference
coverage before choosing Chinese (`zh-CN`). Its download cell requires network
access, `wget` and `tar`, which are available in the intended Colab environment.
Keep raw speaker identifiers and intermediate source-data outputs private.
Only the de-identified final material should be passed to the inference stage.

For local Jupyter, install the notebook dependencies:

```bash
python -m pip install pandas==2.3.3 psutil notebook ipykernel
jupyter notebook
```

Start Jupyter from the repository root and select the environment you installed
into. Pandas 2.3.3 is a setup choice matching the inspected local environment,
not a claim about the original preprocessing environment. The current sampling
code retains grouping columns through `groupby.apply`; do not silently change
that behaviour when changing pandas versions. Record versions for your replay.

## 1. Run notebook 01: prepare the metadata

1. Upload `validated.tsv` and `clip_durations.tsv` to a private Drive folder.
   Open notebook 01 in Colab. To use the pandas version documented here, run
   `%pip install pandas==2.3.3` in a setup cell and restart the runtime, then
   mount Drive using the notebook's first code cell.
2. Set both the directory-listing cell and `DATA_DIR` to that folder. The
   current path is `/content/drive/MyDrive/COMPS760/dataset`.
3. Restart the runtime, then execute the cells in order through the final
   `client_id` check. Keep the original row order and configuration when
   reproducing the frozen sample.
4. The last `nbconvert` cell is an optional HTML export. It refers to an older
   notebook filename on Drive; skip it or supply the actual notebook path.

For local execution, omit the Drive-mount cell, set `DATA_DIR` and the listing
path to your local dataset folder, and provide the downloaded CoVoST TSVs under
`covost2/` in the kernel's working directory. On Windows, the Bash download cell
needs a Bash environment or the same files downloaded and extracted beforehand.

The notebook performs these steps:

1. **Select accent groups.** Use the first pipe-separated self-reported accent
   label. Drop selected rows missing sentence ID, sentence, speaker ID or accent.
2. **Match references and clean clips.** Recover CoVoST English text by audio
   path, then match normalized English sentences to Chinese references. The
   normalization trims, lowercases, collapses whitespace and removes punctuation.
   Apply the original five-group pool's 1st–99th duration percentiles to both
   pools, then reject implausibly long transcripts for their audio duration.
3. **Build the balanced sample.** Add England and United States English to the
   original five groups, cap each speaker at 100 clips per accent, and draw
   600 clips per accent with seed 760.
4. **Export de-identified metadata.** Replace `client_id` with repeating
   pseudonymous speaker IDs (`sample_id`), remove `client_id`, attach the first
   Chinese reference for each normalized sentence, and save the CSV.

Keep `TARGET_LANG = "zh-CN"`, `CAP = 100`, `RANDOM_SEED = 760` and
`N_PER_GROUP = 600` for this experiment. The saved duration thresholds were
approximately 1,728–9,384 ms; they are calculated from the source pool rather
than fixed constants. Unseeded inspection samples do not select the final data.

### Output and checks

The notebook writes `DATA_DIR/final_sample_600_per_group.csv`. Confirm:

- 4,200 rows and seven accent groups, with 600 rows per group.
- No missing `reference_translation_zh` values.
- No `client_id` column; `sample_id` identifies speakers and can repeat.
- Unique selected audio paths and no speaker exceeding the 100-clip cap.

The archived downstream runs record 1,586 speakers. Reproducing the exact sample
also requires the same source files, reference ordering, sampling behaviour and
row order; the seed alone is insufficient. Compare the replay with the frozen
metadata before starting new inference.

## 2. Run notebook 02: extract audio

Copy the exported CSV to your extraction workspace and download the matching
Common Voice audio archive there. The notebook's current archive filename is
`1781724951333-cv-corpus-26.0-2026-06-12-en.tar.gz`; set `TAR_PATH` to the actual
downloaded filename.

There are two independent sections:

| Section | Configuration | Outputs |
|---|---|---|
| `35 clips part` | Set the CSV path, `TAR_PATH` and timing `OUTPUT_DIR` | `timing_test_35_clips.csv`, `timing_test_audio/` |
| `Full clips part` | Set `PROJECT_DIR`, the CSV path, `TAR_PATH` and full `OUTPUT_DIR` | `final_sample_audio/` |

The timing section samples five clips per accent with seed **42** (35 total).
It is separate from the later seven-clip engineering pilot. Its CSV and audio
output paths are relative to the working directory. The full section resets
its variables and extracts every selected audio path.

1. Install pandas and psutil in the selected kernel.
2. Replace the hardcoded `D:/DS/COMPS760_Project` paths with your workspace.
   Also update the timing section's relative CSV path if necessary.
3. On macOS, Linux or Colab, omit the
   `psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)` line. It is a
   Windows process-priority adjustment, not an extraction requirement.
4. Run the timing section if you need the timing pilot, then execute the full
   extraction section in order, including its missing-file and size checks.

The notebook uses streaming TAR extraction and preserves archive member paths.
Depending on the archive layout, MP3s may appear in nested folders rather than
directly under `OUTPUT_DIR`. Its final `glob("*.mp3")` check only counts the
top level, and `min(sizes)` fails if that list is empty. For nested extraction,
use `OUTPUT_DIR.rglob("*.mp3")` in the size-check cell, then prepare the flat
downstream layout below. Check the selected filenames as well as the count.

### Prepare the downstream layout

Copy the metadata and selected recordings into:

```text
data/final_sample/
├── final_sample_600_per_group.csv
└── final_sample_audio/              # selected MP3 files directly in this folder
```

If extraction created nested directories, copy the selected MP3s into the
flat audio folder using the metadata filenames. Check for duplicate basenames
before copying. Confirm all 4,200 expected files exist, no selected file is
empty, and no extra files were accidentally included. The notebook should
report no missing selected paths.

Next, follow [README-running-pipelines.md](README-running-pipelines.md) for
pilot checks, Direct inference and the two Cascade configurations. If you only
need to recalculate results from saved predictions, start with
[README-evaluation.md](README-evaluation.md) instead.

## Contributions and external resources

The [main contribution table](README.md#team-member-contributions) records
**Arizona Xing** for dataset preparation and audio extraction. The project work
includes reference matching, clip filtering, speaker caps, balanced sampling,
de-identification and extraction of the selected audio.

Common Voice supplies the recordings, transcripts and accent metadata; CoVoST 2
supplies the translations. Pandas, Python's `tarfile` and psutil provide library
implementations. Dataset access is linked in the [main README](README.md#provenance);
the CoVoST download URLs are recorded in notebook 01. These datasets and libraries
are external resources. Any copied or adapted implementation snippets should
have their original URL and changes recorded beside the relevant notebook cell.
