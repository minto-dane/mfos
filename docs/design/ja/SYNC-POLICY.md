# MFOS 日本語同期ポリシー

Status: Draft auxiliary policy

## 1. 正本と補助の関係

MFOS の正本は英語です。日本語ドキュメントは、英語正本と同じ構造・同じ ID・同じ意味を持つ補助ミラーです。

日本語ミラーは、英語正本の意味を追加、削除、弱化、強化できません。意味の修正が必要な場合は、先に英語正本を変更します。

## 2. 衝突規則

英語正本と日本語ミラーが矛盾した場合は、英語正本が優先されます。

矛盾した日本語 translation unit は `stale` または `blocked` として扱い、`current` として公開してはいけません。

## 3. 英語のまま保持するもの

次は翻訳しません。

- Requirement ID
- Source Matrix ID
- Test ID
- Evidence ID
- Claim ID
- enum value
- state name
- error code
- ABI name
- API name
- YAML key
- JSON key
- TOML key
- CLI command identifier
- file path
- code block inside schemas or examples
- normative keyword such as `MUST`, `MUST NOT`, `SHOULD`, `MAY`, `UNSUPPORTED`, `SPEC_GAP`, `FAIL-CLOSED`

日本語説明を付ける場合は、英語 keyword を残します。

```text
MUST（必須）
MUST NOT（禁止）
SHOULD（推奨）
MAY（任意）
UNSUPPORTED（仕様はあるが未実装）
SPEC_GAP（仕様未定義）
FAIL-CLOSED（安全側に拒否）
```

## 4. Translation Unit

日本語同期は translation unit 単位で管理します。

形式:

```text
TU-<DOC-ID>-<NNNN>
```

例:

```text
TU-SPEC-00-0001
TU-SPEC-32-0001
TU-TASK-JA-SYNC-0001
```

各 translation unit は、英語正本の hash と日本語ミラーの状態を持ちます。

```yaml
tu_id: TU-SPEC-32-0001
canonical_path: docs/design/specs/32-language-localization.md
source_anchor: "1. Purpose"
source_hash: sha256:<hex>
mirror_path: docs/design/ja/specs/32-language-localization.md
mirror_anchor: "1. 目的"
status: current | stale | partial | blocked | missing
```

## 5. Source Hash

source hash は英語正本の正規化済み translation unit から計算します。

正規化規則:

- UTF-8
- 改行は LF
- 行末空白を削除
- code block は内容を変えない
- ID、enum、error code、state、YAML key はそのまま

英語正本が変わって source hash が変化したら、対応する日本語 unit は `stale` です。

## 6. CI/Lint

CI は最低限、次を検査します。

| Rule ID | 内容 |
| --- | --- |
| LANG-LINT-0001 | 英語正本文書に日本語ミラー entry があること |
| LANG-LINT-0002 | 日本語ミラーが英語正本 path を持つこと |
| LANG-LINT-0003 | translation unit ID が重複しないこと |
| LANG-LINT-0004 | source hash 不一致の unit が `current` を名乗らないこと |
| LANG-LINT-0005 | ID、error code、enum、state、ABI名が変わっていないこと |
| LANG-LINT-0006 | schema/code block が許可なく変わっていないこと |
| LANG-LINT-0007 | 日本語が英語にない normative keyword を追加しないこと |
| LANG-LINT-0008 | 日本語が英語の normative keyword を削除しないこと |
| LANG-LINT-0009 | profile applicability が変わっていないこと |
| LANG-LINT-0010 | audit obligation と fail-closed 条件が変わっていないこと |
| LANG-LINT-0011 | IBM 製品との互換性を主張する表現がないこと |
| LANG-LINT-0014 | machine-readable key が英語のまま保持されていること |
| LANG-LINT-0015 | 日本語で意味修正をした場合、英語正本 patch または ADR があること |

## 7. 更新ワークフロー

英語正本が変わる場合:

1. 英語正本を変更する。
2. 影響する translation unit の source hash を更新する。
3. 日本語 unit を `stale` にする。
4. 日本語を現行英語から再翻訳する。
5. lint を実行する。
6. 意味が一致したら `current` に戻す。

日本語の明瞭化だけを行う場合:

1. 日本語 prose だけを直す。
2. ID、code block、machine-readable key は変えない。
3. source hash は英語正本のまま維持する。
4. lint を実行する。

日本語レビューで仕様の問題を見つけた場合:

1. 日本語文書だけで意味を直さない。
2. 英語正本への patch request を作る。
3. 英語正本が直った後に日本語ミラーを同期する。

## 8. 完全ミラー完了条件

日本語版が完全で同一意味だと主張するには、次を満たす必要があります。

- 対象の英語 Markdown 文書すべてに日本語 mirror path がある。
- 全 translation unit に source hash がある。
- 全日本語 unit が `current` である。
- ID、machine-readable key、code block が保持されている。
- semantic lint が通過している。
- stale、partial、blocked、missing がない。

現時点では、この条件は未達です。
