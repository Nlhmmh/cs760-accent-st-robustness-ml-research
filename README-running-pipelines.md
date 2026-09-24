# Running Pipelines

This guide runs the frozen speech-translation pipelines on a Google Colab GPU
from VS Code. Both use the same 4,200 English audio clips and produce Simplified
Chinese translations. Quality evaluation is performed separately.

| Pipeline | Notebook | Models |
|---|---|---|
| Cascade | [04_cascaded_pipeline.ipynb](notebooks/04_cascaded_pipeline.ipynb) | Whisper large-v2 → NLLB-200 **3.3B** |
| Direct | [03_direct_pipeline.ipynb](notebooks/03_direct_pipeline.ipynb) | SeamlessM4T v2-large |

The archived Cascade run in `runs/cascade_full_run_1788146589/` used NLLB-600M.
It is historical evidence, not a completed run of the current 3.3B configuration.

## Cascade

### Step 1: Connect to Google Colab from VS Code

1. Open this repository in VS Code and install the official
   [Google Colab extension](https://marketplace.visualstudio.com/items?itemName=Google.colab).
2. Open `notebooks/04_cascaded_pipeline.ipynb`.
3. Choose **Select Kernel → Colab → New Colab Server**, sign in when prompted,
   and select an available NVIDIA GPU runtime. A T4 is the hardware used for
   the historical timings below. Avoid a CPU or TPU runtime for this workflow.
4. Confirm that the notebook is connected to the Colab kernel.

The [official extension guide](https://github.com/googlecolab/colab-vscode/wiki/User-Guide)
explains server selection, file uploads, resource monitoring, and Drive mounting.
Your local repository files are separate from the remote runtime filesystem.

Set the working directory in a setup cell on the Colab kernel before pipeline
configuration:

```python
%cd /content
```

Both pipeline notebooks set `PROJECT_ROOT = Path.cwd().resolve()`. With this
layout, it must resolve to `/content`, not `/content/notebooks` or your local
repository path. For local execution, use the repository root instead.

### Step 2: Copy 4,200 samples to the Google Colab environment

The frozen dataset is Git-ignored and must already exist locally:

```text
data/final_sample/
├── final_sample_600_per_group.csv
└── final_sample_audio/              # 4,200 audio clips
```

Create the ZIP with `final_sample/` at its top level, so extraction into
`/content/data` produces the paths expected by the pipeline. From the **local
repository root**, run:

```bash
cd data
python -c "import shutil; shutil.make_archive('../final_sample', 'zip', root_dir='.', base_dir='final_sample')"
cd ..
```

This creates `final_sample.zip` in the repository root. Upload it through the
Google Drive website to the root of **My Drive**. Use Google Drive for this
transfer; uploading the ZIP directly from VS Code to Colab did not work in this
workflow.

Before running the pipeline, execute the following in a setup cell on the
**same Google Colab runtime**:

```python
from google.colab import drive
drive.mount('/content/drive')

!unzip "/content/drive/My Drive/final_sample.zip" -d /content/data
```

Authorize the Drive mount when prompted. If the archive is in a Drive subfolder,
adjust the ZIP path. The resulting layout must be:

```text
/content/data/final_sample/
├── final_sample_600_per_group.csv
└── final_sample_audio/
```

An older ZIP created with `data/final_sample/` at its top level would produce
an extra `data/` directory with this command. Recreate it with the command above
before uploading. If the complete dataset already exists on the runtime, skip
the unzip command. The Cascade notebook no longer contains a dataset extraction
step; prepare the dataset separately using these instructions.

Use the original CSV and audio filenames without regenerating, shuffling, or
editing the data. The notebook validates all 4,200 referenced files and the
7 accent groups × 600 clips balance before inference.

### Step 3: Run the pipeline

Run the notebook's library-installation/import cell first. It currently pins
Transformers to `4.57.6`, PyTorch and torchaudio to `2.11.0`, and torchcodec to
`0.11`. If installation requires a kernel restart, restart before proceeding,
then repeat the imports and set the working directory to `/content` again.
Check that the extracted dataset is still present; if the runtime was replaced,
repeat the Drive mount and extraction. Check for installation errors before
running later cells.

After installation, verify the GPU in a setup cell:

```python
import torch

assert torch.cuda.is_available(), 'Select a GPU Colab runtime before inference.'
print(torch.cuda.get_device_name(0))
print('VRAM (GiB):', torch.cuda.get_device_properties(0).total_memory / 1024**3)
```

Confirm these values in **Constants and Configuration**:

```python
DATASET_MODE = 'final'
WHISPER_MODEL_ID = 'openai/whisper-large-v2'
NLLB_MODEL_ID = 'facebook/nllb-200-3.3B'
RESUME_RUN_DIR = None
CHECKPOINT_EVERY = 10
```

Keep the English transcription setting, `eng_Latn` → `zho_Hans`, seed `760`,
and greedy decoding (`num_beams=1`, `do_sample=False`, `max_new_tokens=256`)
consistent across all samples. CUDA execution uses FP16.

For a pilot first, prepare the inputs with
[create_pilot_samples.ipynb](notebooks/create_pilot_samples.ipynb), transfer
`data/pilot_sample/` to the same relative location under `/content`, and set
`DATASET_MODE = 'pilot'`. Set the working
directory to `/content` manually. After checking the pilot, record the resolved model
SHAs and replace the corresponding `"main"` revision settings with those SHAs
for the final experiment. The 600M model's archived SHA does not apply to 3.3B.

Run the remaining cells in order. The notebook performs:

1. Run-directory creation, environment recording, and dataset validation.
2. Model warm-up and sanity checks.
3. **Pass A:** Whisper transcription of the audio clips.
4. Release of Whisper, then **Pass B:** NLLB translation of the ASR transcripts.
5. Runtime summaries, figures, output saving, and final validation.

NLLB receives the generated ASR transcripts, not the reference English text.
Keep the staged loading: 3.3B weights alone need approximately 6.6 GB
(6.1 GiB) in FP16, plus memory for inference and framework overhead.

A fresh run writes to `/content/runs/cascade_run_<timestamp>/`. Check the final
summary for **4,200 samples, 4,200 successful, and 0 failed**, as well as the
validation results and generation-limit diagnostics. Structural validation can
pass while failures are recorded, so inspect the success/failure counts too.

#### Expected time for 4,200 samples

Budget approximately **2–3 hours on a Tesla T4**, with extra time possible for
initial downloads, installation, and slow storage/network access. This is an
unbenchmarked estimate for the 3.3B model.

The [archived 600M run summary](runs/cascade_full_run_1788146589/run_summary.json)
records 50.9 minutes for Whisper and 14.1 minutes for NLLB on a T4. Assuming
only the NLLB stage becomes 3–6 times slower gives:

```text
50.9 + (14.1 × 3 to 6) ≈ 93–136 minutes of inference
```

The slowdown range is a planning assumption, not a measured confidence interval.
The nominal parameter ratio, 3.3 / 0.6 = 5.5, gives about 129 minutes, but model
size does not predict latency exactly. Different hardware and generated lengths
can change the result. Per-sample timings exclude loading and warm-up.

#### Resume an interrupted run

Preserve the whole run directory, including both prediction/runtime CSVs and
all JSON records. Before restarting, compare its saved model IDs, exact
revisions, decoding settings, and dataset fingerprint with the intended run.
The notebook checks saved metadata when resuming; do not rely on that check to
establish model/configuration compatibility.

Restore the directory under `/content/runs/` if necessary and set, for example:

```python
RESUME_RUN_DIR = Path('/content/runs/cascade_run_1780000000')  # Replace timestamp.
```

Rerun the notebook in order using the same frozen inputs and configuration.
Successful ASR rows are reused, and completed Cascade rows are skipped.
Checkpoints are saved every 10 samples and after failures. Uncheckpointed work
may need to run again.

**Start a fresh directory for NLLB-3.3B; never resume a 600M run as a 3.3B run.**
Files under `/content` need to be copied elsewhere to survive loss of the runtime.

### Step 4: Zip and download the results

After validation and the final run summary, run the notebook's built-in
**22. Zip Run Results — Google Colab Only** cell in the **same notebook/kernel**.
No separate zipping cell is needed for the Cascade pipeline.

It archives the current `RUN_DIR` to `/content/cascade_run_<timestamp>.zip`,
checks ZIP integrity, and prints `Results archive:` with the resulting path.
The ZIP contains the run directory and its saved files. The cell automatically
skips outside Google Colab. Rerunning it replaces the ZIP for that run.

Creating the ZIP under `/content` does not make it a persistent backup. Keep
the kernel active for the following copy step, which uses `archive_path`,
`Path`, and `shutil` from the archiving cell.

For a persistent copy, use **Colab: Mount Google Drive to Server...** from the
VS Code command palette, execute its appended mount cell, and then copy the ZIP:

```python
backup_dir = Path('/content/drive/MyDrive/CS760/pipeline_runs')
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(archive_path, backup_dir / archive_path.name)
print('Saved to Drive:', backup_dir / archive_path.name)
```

Download the ZIP from Google Drive to your computer and extract it into the
local repository's `runs/` directory. Retain its unique timestamp directory.
Also save the executed notebook in VS Code to preserve its outputs.

The archive should contain:

```text
cascade_run_<timestamp>/
├── cascade_predictions.csv       # Metadata, id, ASR transcript, translation
├── cascade_runtime.csv           # Per-sample timings, statuses, diagnostics
├── run_config.json
├── run_environment.json
├── run_summary.json
├── runtime_per_clip.png
└── runtime_vs_audio_duration.png
```

Confirm these files exist locally before ending the runtime. A saved notebook
alone does not include the CSV/JSON artifacts.

## Direct

Use the same connection, dataset upload, working-directory, and archive steps
with [03_direct_pipeline.ipynb](notebooks/03_direct_pipeline.ipynb). Run it in a
separate GPU session or after releasing the Cascade models.

If the dataset is already extracted on the same server, reuse it. On a fresh
server, follow Step 2 to mount Google Drive and extract `final_sample.zip` into
`/content/data`, then set the working directory to `/content` before configuration.

Confirm its configuration:

```python
DATASET_MODE = 'final'
MODEL_ID = 'facebook/seamless-m4t-v2-large'
MODEL_REVISION = '5f8cc790b19fc3f67a61c105133b20b34e3dcb76'
TARGET_LANGUAGE = 'cmn'
RESUME_RUN_DIR = None
```

Use its own installation cell and execute the notebook in order. It writes
`direct_predictions.csv`, `direct_runtime.csv`, JSON records, and runtime figures
to `/content/runs/direct_run_<timestamp>/`. The Direct notebook does not include
the final archiving cell. Copy the code cell from section 22 of the Cascade
notebook to the end of the Direct notebook and run it after validation in the
Direct kernel. It uses that kernel's `RUN_DIR` and creates
`/content/direct_run_<timestamp>.zip`, with the same Colab-only check. Then
follow the Drive copy and download instructions above.

The [historical Direct run](runs/direct_full_run_1788151795/run_summary.json)
measured about 65 minutes of per-sample inference on a T4; allow additional
time for setup, loading, and saving. Confirm all 4,200 samples succeeded and
inspect generation diagnostics before using a new run downstream.

## After both runs

Use [combine_translation_outputs.ipynb](notebooks/combine_translation_outputs.ipynb)
to combine the selected runs. Review its input paths first so it uses the new
3.3B Cascade results rather than the archived 600M results. That notebook expects
to run from `notebooks/`.

Confirm matching dataset fingerprints and join predictions using the unique
clip `id`. `sample_id` is a pseudonymous speaker identifier and can repeat.
Keep the original run artifacts alongside the combined output for traceability.
WER, chrF++, BLEU, and statistical analyses are separate from pipeline execution.

## Troubleshooting

| Symptom | Action |
|---|---|
| Metadata or audio not found | Check the remote `/content/data/final_sample/` layout and `PROJECT_ROOT`; local files are not automatically visible remotely. |
| CUDA unavailable | Select a GPU Colab server and verify the installed PyTorch build before inference. |
| Import or audio-decoding errors after installation | Check installation output and package compatibility; restart the kernel after package changes, then rerun setup/imports. |
| GPU out of memory | Stop other GPU workloads and use a clean runtime; preserve the staged model release and FP16 settings. Use a larger GPU if necessary. |
| Runtime disconnects | Restore a preserved checkpoint directory and resume with the same models, revisions, settings, and input data. |
| Nonzero failed samples | Inspect the stage status/error columns in the runtime CSV; resolve the cause before treating the run as complete. |
| Resume metadata mismatch | Restore the exact frozen CSV and row order, or start a fresh run; do not bypass the check. |
