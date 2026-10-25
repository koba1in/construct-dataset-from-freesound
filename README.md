# Construct Dataset from Freesound

Hugging Face 上で公開されている [benjamin-paine/freesound-laion-640k](https://huggingface.co/datasets/benjamin-paine/freesound-laion-640k) から、指定したライセンスの音声データをフィルタリング・リサンプリングしながらダウンロード・ローカル保存する CLI ツールです。

巨大なデータセット全体を事前にダウンロードすることなく、**ストリーミング形式で必要な音声のみを逐次取得・変換して保存**します。

---

## 主な特徴

- **CLI ツール化**: インストール後、専用コマンド `construct-dataset-from-freesound` から簡単に実行可能
- **複数 split・複数ライセンス一括指定**: `train` や `test` をまとめて指定し、自動で split ごとのフォルダに分類保存
- **ストリーミング取得**: ローカルストレージを圧迫せず、条件に合致するデータのみを順次処理
- **音声フォーマットの統一**: 16kHz モノラル / 16-bit PCM FLAC 形式へ自動変換
- **エラー耐性**: 破損データや読み込みエラーが発生した音声は自動でログ出力してスキップし、ダウンロード処理を継続
- **環境変数の `.env` 対応**: `python-dotenv` により `.env` ファイルからのトークン読み込みをサポート

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

データセットへのアクセスに必要な Hugging Face のアクセストークン（Read 権限）を設定します。

#### 方法 A: `.env` ファイルを作成する（推奨）
プロジェクト直下に `.env` ファイルを作成し、トークンを記述します：
```env
HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### 方法 B: 環境変数に設定する
- **Linux / macOS (bash, zsh):**
  ```bash
  export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```
- **Windows (PowerShell):**
  ```powershell
  $env:HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```

---

## 実行方法

インストール後、以下のコマンドで実行します。

```bash
# uv を使用する場合
uv run construct-dataset-from-freesound -s <split...> -p <output_dir> -l <license...>

# pip (venv 有効化時) の場合
construct-dataset-from-freesound -s <split...> -p <output_dir> -l <license...>
```

### オプション一覧

| オプション | 省略形 | 必須 | 説明 | 指定例 |
| :--- | :--- | :---: | :--- | :--- |
| `--split` | `-s` | ○ | 対象の split（複数指定可能） | `train` または `train test` |
| `--path` | `-p` | ○ | 保存先のルートディレクトリ | `./data` |
| `--license` | `-l` | ○ | 対象のライセンス（複数指定可能） | `CC0-1.0 CC-BY-4.0` |

#### 指定可能なライセンス一覧
- `CC0-1.0`
- `CC-BY-4.0`
- `CC-BY-3.0`
- `CC-BY-NC-3.0`
- `CC-BY-NC-4.0`
- `CC-Sampling+`

---

## 実行例

### 例1: `train` の商用利用可能な音声 (CC0 & CC-BY) をダウンロード
```bash
uv run construct-dataset-from-freesound -s train -p ./dataset -l CC0-1.0 CC-BY-4.0 CC-BY-3.0
```

### 例2: `train` と `test` 両方の CC0 データを一括ダウンロード
```bash
uv run construct-dataset-from-freesound -s train test -p ./dataset -l CC0-1.0
```

### 出力ディレクトリ構成
指定した `--path` の下に各 split のディレクトリが自動作成され、音声が保存されます：
```text
dataset/
├── train/
│   ├── 12345.flac
│   ├── 12346.flac
│   └── ...
└── test/
    ├── 98765.flac
    └── ...
```

---

## 注意事項

- **ダウンロード済みファイルのスキップ**: 指定ディレクトリに既に `{freesound_id}.flac` が存在する場合は自動的にスキップされます。処理が中断された場合でも同じコマンドで安全に再開できます。
- **音声データのライセンス**: ダウンロードされた各音声の著作権およびライセンスは、Freesound の各クリエイターに帰属します。商用利用・再配布などの際は各ファイルのライセンス条項（CC-BY の attribution 等）をご確認ください。

---

## ライセンス

本ツールのソースコードは [MIT License](LICENSE) の下で公開されています。
