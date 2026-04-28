# MFOS

MFOS は、IBM が公開している z/OS / IBM Z 関連文書を参照資料として使う、
z/OS-inspired enterprise OS の設計・実装プロジェクトです。
IBM による承認、提携、後援、z/OS 互換、IBM 製品互換、API 互換は主張しません。

現時点の正本は [docs/design](docs/design/) にあります。今回追加したトップレベルの
ディレクトリは、既存 docs を移動せず、今後の実装・検証・証拠・AI 作業を迷わず置くための
作業レイヤです。

重要な入口:

- 設計正本: [docs/design/mfos-design.md](docs/design/mfos-design.md)
- Source Card: [docs/design/source-matrix/cards](docs/design/source-matrix/cards)
- 要件レジストリ: [docs/design/registries/requirements.yaml](docs/design/registries/requirements.yaml)
- 作業状態: [docs/design/STATUS.md](docs/design/STATUS.md)

英語正本・日本語補助の規則に従い、機械可読 ID、enum、error code、ABI 名、要件本文は英語を正本にします。
