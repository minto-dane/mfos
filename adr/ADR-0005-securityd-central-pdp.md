# ADR-0005: securityd Is the Central PDP

`securityd` is the central policy decision point for protected resources.
Services such as `datasetd`, `spoold`, `jobd`, and `operatord` must not make
final authorization decisions independently.

