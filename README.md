# Construct Dataset from Freesound

Hugging Face 上で公開されている [benjamin-paine/freesound-laion-640k](https://huggingface.co/datasets/benjamin-paine/freesound-laion-640k) から、指定したライセンスの音声データをフィルタリング・リサンプリングしながらダウンロード・ローカル保存するツールです。

巨大なデータセット全体を事前にダウンロードすることなく、**ストリーミング形式で必要な音声のみを逐次取得・変換して保存**します。

---

## 主な特徴

- **ストリーミング取得**: ローカルストレージを圧迫せず、必要なデータのみを順次処理
- **ライセンス指定フィルタ**: CC0やCC-BYなど、用途に合わせて特定のライセンスの音声のみを抽出可能
- **音声フォーマットの統一**: 16kHz モノラル / 16-bit PCM FLAC 形式へ自動変換

---

## 音声の保存フォーマット（デフォルト）

| 項目 | 設定値 |
| :--- | :--- |
| **サンプリングレート** | 16,000 Hz |
| **チャンネル数** | 1 (Mono) |
| **フォーマット** | FLAC (Free Lossless Audio Codec) |
| **サブタイプ** | Signed 16-bit PCM (`PCM_16`) |
| **ファイル名規則** | `{freesound_id}.flac` |

---

## 必要要件 & セットアップ

Python 3.10 以上が必要です。パッケージマネージャーには [uv](https://github.com/astral-sh/uv) を推奨しています。

### 1. リポジトリのクローンと環境構築

```bash
git clone https://github.com/<your-username>/construct-dataset-from-freesound.git
cd construct-dataset-from-freesound

# uv を使用する場合
uv sync

# または pip を使用する場合
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Hugging Face トークンの設定

データセットへのアクセスに必要な Hugging Face のアクセストークン（Read 権限）を環境変数 `HF_TOKEN` に設定します。

**Linux / macOS (bash, zsh):**
```bash
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 実行方法

`scripts/download_audio.py` を以下の引数を指定して実行します。

```bash
uv run python scripts/download_audio.py <split> <output_dir> <license_1> [license_2 ...]
```
*(pip 環境の場合は `python scripts/download_audio.py ...`)*

### 引数の説明

1. **`split`**: ダウンロードするデータセットの分割
   - `train` または `test`
2. **`output_dir`**: 音声ファイルの保存先ディレクトリパス
3. **`licenses`** (第3引数以降・複数指定可): ダウンロード対象とするライセンス名

#### 指定可能なライセンス一覧
- `CC0-1.0`
- `CC-BY-4.0`
- `CC-BY-3.0`
- `CC-BY-NC-3.0`
- `CC-BY-NC-4.0`
- `CC-Sampling+`

---

## 実行例

### 例1: 商用利用可能な音声を `train` からダウンロードする場合 (CC0 & CC-BY)
```bash
uv run python scripts/download_audio.py train ./dataset/train CC0-1.0 CC-BY-4.0 CC-BY-3.0
```

### 例2: パブリックドメイン (CC0) のテストデータのみをダウンロードする場合
```bash
uv run python scripts/download_audio.py test ./dataset/test CC0-1.0
```

---

## 注意事項

- **ダウンロード済みファイルのスキップ**: 指定したディレクトリに既に `{freesound_id}.flac` が存在する場合は自動的にスキップされます。途中で処理が中断された場合でも再実行が可能です。
- **音声データのライセンス**: ダウンロードされた各音声の著作権およびライセンスは、Freesound の各クリエイターに帰属します。商用利用・再配布などの際は各ファイルのライセンス条項（CC-BY の attribution 等）をご確認ください。

---

