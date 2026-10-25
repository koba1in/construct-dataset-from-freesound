# Construct Dataset from Freesound

Hugging Face の [`benjamin-paine/freesound-laion-640k`](https://huggingface.co/datasets/benjamin-paine/freesound-laion-640k) から、指定した split とライセンスの音声をストリーミングで取得し、リサンプリングして保存する CLI ツールです。

音声は `soundfile` で読み込み、ステレオなど複数チャンネルの音声はチャンネル方向に平均してモノラル化します。その後、16 kHz にリサンプリングし、16-bit PCM の FLAC として保存します。

## 必要環境

- Python 3.10 以上
- [uv](https://docs.astral.sh/uv/)（推奨）または pip
- Hugging Face の Read アクセストークン

## インストール

リポジトリを取得して、プロジェクトのルートで依存関係をインストールします。

```bash
git clone https://github.com/koba1in/construct-dataset-from-freesound.git
cd construct-dataset-from-freesound
uv sync
```

pip を使う場合は、仮想環境を有効にしてからインストールします。

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Hugging Face トークン

CLI は `HF_TOKEN` を環境変数から読み込みます。プロジェクトルートに `.env` ファイルを置く場合は、次の形式で記述してください。

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

または、シェルで環境変数を設定します。

```bash
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Windows PowerShell の場合:

```powershell
$env:HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

トークンを含む `.env` は公開リポジトリへ登録しないでください。

## 実行

```bash
uv run construct-dataset-from-freesound \
  --split train test \
  --path ./dataset \
  --license CC0-1.0 CC-BY-4.0
```

pip でインストールした場合は、仮想環境を有効にして次のように実行します。

```bash
construct-dataset-from-freesound \
  --split train \
  --path ./dataset \
  --license CC0-1.0
```

### オプション

| オプション | 必須 | 説明 |
| --- | :---: | --- |
| `--split`, `-s` | はい | 対象 split。複数指定できます（例: `train test`）。 |
| `--path`, `-p` | はい | 保存先のルートディレクトリ。split ごとのサブディレクトリが作られます。 |
| `--license`, `-l` | はい | 対象ライセンス。複数指定できます。 |

このリポジトリで指定可能なライセンス名:

- `CC0-1.0`
- `CC-BY-4.0`
- `CC-BY-3.0`
- `CC-BY-NC-3.0`
- `CC-BY-NC-4.0`
- `CC-Sampling+`

出力例:

```text
dataset/
├── train/
│   └── <freesound_id>.flac
└── test/
    └── <freesound_id>.flac
```

## 出力形式と再実行

- サンプリングレート: 16,000 Hz
- チャンネル: モノラル
- 形式: FLAC、PCM 16-bit
- ファイル名: `<freesound_id>.flac`

同じ名前のファイルが保存先にすでにある場合、そのファイルはスキップされます。ファイルの内容や完全性は検査しないため、異常終了で不完全なファイルが残った場合は、該当ファイルを削除してから再実行してください。

音声の取得・デコードに失敗したサンプルはログに警告を出してスキップします。`soundfile` が読める形式は、実行環境に含まれる libsndfile の対応状況にも依存します。

## ライセンス

このツールのソースコードは MIT License で公開されています。取得した音声には各クリエイターのライセンスが適用されます。利用・再配布時は個々のライセンス条件（CC-BY の表示義務など）を確認してください。
