# MFOS 日本語ドキュメント入口

Status: Initial Japanese index

## 1. 位置づけ

MFOS の正本仕様は英語です。日本語ドキュメントは、レビュー、実装支援、運用理解のための補助ミラーです。

日本語ミラーは完全性を目標にしますが、日本語テキストは英語正本の意味を変更できません。英語正本と日本語ミラーが衝突した場合は、英語正本が優先されます。

## 2. 基本規則

- 英語正本: `docs/design/**/*.md`
- 日本語ミラー: `docs/design/ja/**/*.md`
- 機械可読キー: 英語のまま保持
- Requirement ID、Source ID、Test ID、Evidence ID: 英語のまま保持
- enum、state、error code、ABI名、YAML key: 英語のまま保持
- 日本語で意味の修正が必要な場合: 先に英語正本を修正

詳細な同期規則は [SYNC-POLICY.md](SYNC-POLICY.md) を参照してください。

## 3. 初期日本語インデックス

このインデックスは、日本語ミラー作成対象を定義します。現時点では全翻訳を作成していません。`sync_status` が `missing` または `partial` の文書は未完成です。

| English canonical | Japanese mirror | sync_status |
| --- | --- | --- |
| `docs/design/README.md` | `docs/design/ja/README.md` | partial |
| `docs/design/STATUS.md` | `docs/design/ja/STATUS.md` | missing |
| `docs/design/mfos-design.md` | `docs/design/ja/mfos-design.md` | missing |
| `docs/design/specs/00-normative-language.md` | `docs/design/ja/specs/00-normative-language.md` | missing |
| `docs/design/specs/01-glossary.md` | `docs/design/ja/specs/01-glossary.md` | missing |
| `docs/design/specs/02-source-matrix.md` | `docs/design/ja/specs/02-source-matrix.md` | missing |
| `docs/design/specs/03-system-integrity.md` | `docs/design/ja/specs/03-system-integrity.md` | missing |
| `docs/design/specs/04-threat-model.md` | `docs/design/ja/specs/04-threat-model.md` | missing |
| `docs/design/specs/05-object-model.md` | `docs/design/ja/specs/05-object-model.md` | missing |
| `docs/design/specs/06-authorization.md` | `docs/design/ja/specs/06-authorization.md` | missing |
| `docs/design/specs/07-audit.md` | `docs/design/ja/specs/07-audit.md` | missing |
| `docs/design/specs/08-dataset-catalog.md` | `docs/design/ja/specs/08-dataset-catalog.md` | missing |
| `docs/design/specs/09-job-spool.md` | `docs/design/ja/specs/09-job-spool.md` | missing |
| `docs/design/specs/10-operator-console.md` | `docs/design/ja/specs/10-operator-console.md` | missing |
| `docs/design/specs/11-workload-policy.md` | `docs/design/ja/specs/11-workload-policy.md` | missing |
| `docs/design/specs/12-amf.md` | `docs/design/ja/specs/12-amf.md` | missing |
| `docs/design/specs/13-update.md` | `docs/design/ja/specs/13-update.md` | missing |
| `docs/design/specs/14-nucleus.md` | `docs/design/ja/specs/14-nucleus.md` | missing |
| `docs/design/specs/15-svc-pcall.md` | `docs/design/ja/specs/15-svc-pcall.md` | missing |
| `docs/design/specs/16-pxm.md` | `docs/design/ja/specs/16-pxm.md` | missing |
| `docs/design/specs/17-guard.md` | `docs/design/ja/specs/17-guard.md` | missing |
| `docs/design/specs/18-linux-gateway.md` | `docs/design/ja/specs/18-linux-gateway.md` | missing |
| `docs/design/specs/19-assurance-case.md` | `docs/design/ja/specs/19-assurance-case.md` | missing |
| `docs/design/specs/20-conformance.md` | `docs/design/ja/specs/20-conformance.md` | missing |
| `docs/design/specs/21-ai-implementation-contract.md` | `docs/design/ja/specs/21-ai-implementation-contract.md` | missing |
| `docs/design/specs/22-production-readiness.md` | `docs/design/ja/specs/22-production-readiness.md` | missing |
| `docs/design/specs/23-requirements-catalog.md` | `docs/design/ja/specs/23-requirements-catalog.md` | missing |
| `docs/design/specs/24-formal-methods.md` | `docs/design/ja/specs/24-formal-methods.md` | missing |
| `docs/design/specs/25-operations-recovery.md` | `docs/design/ja/specs/25-operations-recovery.md` | missing |
| `docs/design/specs/26-hardware-profile.md` | `docs/design/ja/specs/26-hardware-profile.md` | missing |
| `docs/design/specs/27-spec-front-matter.md` | `docs/design/ja/specs/27-spec-front-matter.md` | missing |
| `docs/design/specs/28-machine-readable-registries.md` | `docs/design/ja/specs/28-machine-readable-registries.md` | missing |
| `docs/design/specs/29-test-strategy.md` | `docs/design/ja/specs/29-test-strategy.md` | missing |
| `docs/design/specs/30-attestation-measured-boot.md` | `docs/design/ja/specs/30-attestation-measured-boot.md` | missing |
| `docs/design/specs/31-release-distribution-rollback.md` | `docs/design/ja/specs/31-release-distribution-rollback.md` | missing |
| `docs/design/specs/32-language-localization.md` | `docs/design/ja/specs/32-language-localization.md` | missing |
| `docs/design/specs/INDEX.md` | `docs/design/ja/specs/INDEX.md` | missing |
| `docs/design/source-matrix/source-matrix.md` | `docs/design/ja/source-matrix/source-matrix.md` | missing |
| `docs/design/source-matrix/source-lint-spec.md` | `docs/design/ja/source-matrix/source-lint-spec.md` | missing |
| `docs/design/source-matrix/traceability-index.md` | `docs/design/ja/source-matrix/traceability-index.md` | missing |
| `docs/design/source-matrix/traceability-policy.md` | `docs/design/ja/source-matrix/traceability-policy.md` | missing |
| `docs/design/packs/PACKS.md` | `docs/design/ja/packs/PACKS.md` | missing |
| `docs/design/prompts/ai-prompts.md` | `docs/design/ja/prompts/ai-prompts.md` | missing |
| `docs/design/registries/README.md` | `docs/design/ja/registries/README.md` | missing |
| `docs/design/assurance/assurance-case-template.md` | `docs/design/ja/assurance/assurance-case-template.md` | missing |
| `docs/design/assurance/claim-registry-spec.md` | `docs/design/ja/assurance/claim-registry-spec.md` | missing |
| `docs/design/assurance/evidence-archive-spec.md` | `docs/design/ja/assurance/evidence-archive-spec.md` | missing |
| `docs/design/assurance/formal-model-plan.md` | `docs/design/ja/assurance/formal-model-plan.md` | missing |
| `docs/design/assurance/operator-runbooks.md` | `docs/design/ja/assurance/operator-runbooks.md` | missing |
| `docs/design/assurance/operator-training-drills.md` | `docs/design/ja/assurance/operator-training-drills.md` | missing |
| `docs/design/assurance/release-review-workflow.md` | `docs/design/ja/assurance/release-review-workflow.md` | missing |
| `docs/design/tasks/implementation-roadmap.md` | `docs/design/ja/tasks/implementation-roadmap.md` | missing |
| `docs/design/tasks/spec-front-matter-migration.md` | `docs/design/ja/tasks/spec-front-matter-migration.md` | missing |
| `docs/design/tasks/test-taxonomy.md` | `docs/design/ja/tasks/test-taxonomy.md` | missing |
| `docs/design/tasks/work-breakdown.md` | `docs/design/ja/tasks/work-breakdown.md` | missing |
| `docs/design/tasks/japanese-doc-sync.md` | `docs/design/ja/tasks/japanese-doc-sync.md` | missing |

## 4. 現在の制限

- この変更では全ドキュメントの翻訳は行いません。
- まだ translation unit manifest は実装されていません。
- source hash を生成する CI/lint 実装は未作成です。
- translation unit manifest と language lint が実装されるまで、`sync_status: current` を正式には主張しません。この文書は初期インデックスです。

## 5. 日本語作業時の最短手順

1. 英語正本を確認する。
2. 翻訳対象の translation unit ID を割り当てる。
3. 英語 source hash を記録する。
4. ID、enum、error code、YAML key、code block を保持して翻訳する。
5. 意味の変更が必要なら日本語では直さず、英語正本の修正タスクにする。
6. lint を通して `sync_status` を更新する。
