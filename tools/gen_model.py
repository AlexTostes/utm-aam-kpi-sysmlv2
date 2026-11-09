"""Gera o modelo SysML v2 dos 31 KPIs candidatos (artigo 1, Tabelas 3 e 4).

Saidas: KPI_Framework.sysml (todos os pacotes) e cells.json (um pacote por celula,
na ordem de dependencia), usado depois para montar o notebook.
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "e1"))
from matrix import UTM as E1_UTM, AAM as E1_AAM
E1 = {r[0]: r for r in E1_UTM + E1_AAM}
SRC = {"NS": "NetworkShared", "PA": "ProviderArchived", "IH": "InternallyHeld", "NA": "NotAddressed"}

OUT = sys.argv[1]

KPAS = [
    ("AccessAndEquity", "Access and Equity"),
    ("Capacity", "Capacity"),
    ("CostEffectiveness", "Cost Effectiveness"),
    ("Efficiency", "Efficiency"),
    ("Environment", "Environment"),
    ("Flexibility", "Flexibility"),
    ("GlobalInteroperability", "Global Interoperability"),
    ("Participation", "ATM Community Participation"),
    ("Predictability", "Predictability"),
    ("Safety", "Safety"),
    ("Security", "Security"),
]

# KPA -> Performance Objective (texto do artigo 1), por dominio
UTM_PO = {
    "AccessAndEquity": "Promote equitable access to UTM-enabled operations among eligible users.",
    "Capacity": "Accommodate valid operational demand within the available UTM operational environment.",
    "CostEffectiveness": "Provide UTM services with efficient use of attributable system resources.",
    "Efficiency": "Minimize operational inefficiencies attributable to UTM constraints and decisions.",
    "Environment": "Limit environmental burden attributable to UTM-related operational decisions.",
    "Flexibility": "Maintain operational adaptability and continuity under changing or degraded conditions.",
    "GlobalInteroperability": "Enable effective operational interaction and information exchange among UTM actors and services.",
    "Participation": "Enable meaningful participation of relevant stakeholders in UTM-related processes and decisions.",
    "Predictability": "Provide predictable operational outcomes with respect to planned timing.",
    "Safety": "Maintain acceptable operational safety for airborne operations and affected third parties.",
    "Security": "Protect UTM operations, services, and information against security compromise.",
}
AAM_PO = {
    "AccessAndEquity": "Promote equitable and practical access to AAM transportation for the intended population.",
    "Capacity": "Accommodate transportation demand within the integrated AAM operational system.",
    "CostEffectiveness": "Provide AAM transportation with efficient use of attributable system resources.",
    "Efficiency": "Improve end-to-end transportation efficiency while minimizing operational delay.",
    "Environment": "Limit environmental burden associated with AAM transportation and operations.",
    "Flexibility": "Maintain operational adaptability and continuity under changing or degraded conditions.",
    "GlobalInteroperability": "Enable effective operational interoperability among AAM actors, systems, and infrastructure.",
    "Participation": "Ensure meaningful engagement of relevant and affected AAM stakeholders.",
    "Predictability": "Provide predictable operational outcomes with respect to planned timing.",
    "Safety": "Maintain acceptable operational safety for AAM users and affected third parties.",
    "Security": "Protect AAM operations, systems, information, and stakeholders against security-related harm.",
}
UTM_APPLIC = {k: "Applicable" for k, _ in KPAS}
UTM_APPLIC["Environment"] = "ConditionallyApplicable"
AAM_APPLIC = {k: "Applicable" for k, _ in KPAS}

# (codigo, nome do calc def, titulo do artigo, KPA, construto, status, operacionalizacao, padrao)
UTM_KPIS = [
    ("UTM-AE-01", "EquitableAccessGap", "Equitable Access Gap", "AccessAndEquity", "Between-Group Access Disparity", "P", "Pending", None),
    ("UTM-CAP-01", "DemandAccommodationRate", "Demand Accommodation Rate", "Capacity", "Demand Accommodation", "P", "ProposedInThisStudy", "AccommodationRate"),
    ("UTM-CE-01", "ServiceCostPerManagedOperation", "UTM Service Cost per Managed Operation", "CostEffectiveness", "Unit UTM Service Cost", "P", "Pending", None),
    ("UTM-EFF-01", "AttributableOperationalDelay", "UTM-Attributable Operational Delay", "Efficiency", "UTM-Attributable Temporal Inefficiency", "P", "Pending", None),
    ("UTM-EFF-02", "InducedTrajectoryExtension", "UTM-Induced Trajectory Extension", "Efficiency", "UTM-Attributable Spatial Inefficiency", "P", "Pending", None),
    ("UTM-ENV-01", "InducedEnergyPenalty", "UTM-Induced Energy Penalty", "Environment", "UTM-Attributable Marginal Energy Burden", "C", "ConceptualFormulaInArticle1", "ENV"),
    ("UTM-FLEX-01", "SuccessfulReplanningRate", "Successful Replanning Rate", "Flexibility", "Successful Operational Adaptation", "P", "Pending", None),
    ("UTM-FLEX-02", "DegradedServiceContinuityRate", "Degraded-Service Continuity Rate", "Flexibility", "Essential Service Continuity Under Degradation", "P", "Pending", None),
    ("UTM-GI-01", "SuccessfulInformationExchangeRate", "Successful Operational Information Exchange Rate", "GlobalInteroperability", "Fit-for-Purpose Operational Information Exchange", "P", "Pending", None),
    ("UTM-PART-01", "EffectiveStakeholderParticipationRate", "Effective Stakeholder Participation Rate", "Participation", "Effective Stakeholder Participation", "P", "Pending", None),
    ("UTM-PRED-01", "OperationTimePredictabilityRate", "Operation-Time Predictability Rate", "Predictability", "Temporal Predictability", "P", "ProposedInThisStudy", "TemporalConformanceRate"),
    ("UTM-SAF-01", "SeparationSafetyEventRate", "Separation-Safety Event Rate", "Safety", "Separation-Related Safety Event Frequency", "P", "Pending", None),
    ("UTM-SAF-02", "InfluencedGroundThirdPartyRisk", "UTM-Influenced Ground Third-Party Risk", "Safety", "UTM-Influenced Ground Third-Party Risk", "P", "Pending", None),
    ("UTM-SEC-01", "SecurityCompromiseRate", "Security Compromise Rate", "Security", "Operational Security Compromise Frequency", "P", "Pending", None),
]
AAM_KPIS = [
    ("AAM-AE-01", "PopulationServiceAccessibility", "Population Service Accessibility", "AccessAndEquity", "Geographic Accessibility", "P", "Pending", None),
    ("AAM-AE-02", "AffordabilityBurdenRatio", "Affordability Burden Ratio", "AccessAndEquity", "Economic Accessibility", "P", "Pending", None),
    ("AAM-CAP-01", "IntegratedDemandAccommodationRate", "Integrated Demand Accommodation Rate", "Capacity", "Integrated Demand Accommodation", "P", "ProposedInThisStudy", "AccommodationRate"),
    ("AAM-CE-01", "CostPerCompletedOperation", "Cost per Completed AAM Operation", "CostEffectiveness", "Cost per Completed Operational Output", "P", "Pending", None),
    ("AAM-EFF-01", "DoorToDoorTravelTimeBenefit", "Door-to-Door Travel-Time Benefit", "Efficiency", "Door-to-Door Travel Efficiency", "P", "Pending", None),
    ("AAM-EFF-02", "MeanOperationalDelay", "Mean AAM Operational Delay", "Efficiency", "Operational Delay", "P", "Pending", None),
    ("AAM-ENV-01", "LifeCycleGHGIntensity", "Life-Cycle GHG Intensity", "Environment", "Climate Impact", "P", "Pending", None),
    ("AAM-ENV-02", "CommunityNoiseExposure", "Community Noise Exposure", "Environment", "Community Noise Impact", "P", "Pending", None),
    ("AAM-FLEX-01", "SuccessfulReplanningRate", "Successful Operational Replanning Rate", "Flexibility", "Operational Replanning", "P", "Pending", None),
    ("AAM-FLEX-02", "DegradedOperationContinuityRate", "Degraded-Operation Continuity Rate", "Flexibility", "Operational Continuity", "P", "Pending", None),
    ("AAM-GI-01", "SuccessfulInteroperabilityRate", "Successful Operational Interoperability Rate", "GlobalInteroperability", "Operational Interoperability Success", "P", "Pending", None),
    ("AAM-PART-01", "EffectiveEngagementCoverage", "Effective Stakeholder Engagement Coverage", "Participation", "Effective Engagement Coverage", "P", "Pending", None),
    ("AAM-PRED-01", "OperationalPunctuality", "Operational Punctuality", "Predictability", "Temporal Predictability", "P", "ProposedInThisStudy", "TemporalConformanceRate"),
    ("AAM-SAF-01", "SafetyOccurrenceRateBySeverity", "Safety Occurrence Rate by Severity", "Safety", "Operational Safety Occurrence", "P", "Pending", None),
    ("AAM-SAF-02", "GroundThirdPartyRisk", "Ground Third-Party Risk", "Safety", "Ground Third-Party Risk", "P", "Pending", None),
    ("AAM-SEC-01", "CybersecurityCompromiseRate", "Cybersecurity Compromise Rate", "Security", "Cybersecurity Compromise", "P", "Pending", None),
    ("AAM-SEC-02", "PrivacyIncidentRate", "Privacy Incident Rate", "Security", "Privacy Compromise", "P", "Pending", "EXT"),
]

# Metricas diagnosticas citadas no artigo 1 (Sec. 4.5)
UTM_DIAG = ("SuccessfulInformationExchangeRate", [
    ("ExchangeLatency", "Latency of operational information exchange"),
    ("MessageLoss", "Message loss"),
    ("APICallSuccess", "API call success"),
    ("InformationAge", "Age of operational information"),
    ("InformationConsistency", "Consistency of shared operational information"),
])
AAM_DIAG = ("IntegratedDemandAccommodationRate", [
    ("VertiportThroughput", "Vertiport throughput"),
    ("PadUtilization", "Pad utilization"),
    ("ChargingAvailability", "Charging availability"),
    ("AirspaceConstraints", "Airspace constraints"),
    ("FleetAvailability", "Fleet availability"),
])

STATUS = {"P": "ProvisionallyRetained", "C": "ConditionallyRetained"}
I = "    "


def pkg(name, doc, imports, body):
    lines = [f"package {name} {{", f"{I}doc /* {doc} */"]
    lines += [f"{I}private import {imp}::*;" for imp in imports]
    lines.append("")
    lines += body
    lines.append("}")
    return "\n".join(lines)


cells = []

# 1. Taxonomia e metadados
cells.append(("KPI_Taxonomy", pkg("KPI_Taxonomy",
    "Enumerations and metadata used to classify KPAs, performance objectives and KPI candidates "
    "(article 1: applicability, analytical status, measurement maturity, taxonomic fit).",
    ["ScalarValues"], [
    f"{I}enum def Domain {{ enum UTM; enum AAM; }}",
    f"{I}enum def Applicability {{ enum Applicable; enum ConditionallyApplicable; enum NotApplicable; }}",
    f"{I}enum def RetentionStatus {{ enum ProvisionallyRetained; enum ConditionallyRetained; }}",
    f"{I}enum def Operationalization {{",
    f"{I}{I}doc /* Measurement maturity of the candidate, kept distinct from retention status (article 1). */",
    f"{I}{I}enum ConceptualFormulaInArticle1;",
    f"{I}{I}enum ProposedInThisStudy;",
    f"{I}{I}enum Pending;",
    f"{I}}}",
    f"{I}enum def TaxonomicFit {{ enum Direct; enum Provisional; enum Gap; }}",
    "",
    f"{I}metadata def KPAApplicability {{",
    f"{I}{I}attribute domain : Domain;",
    f"{I}{I}attribute applicability : Applicability;",
    f"{I}}}",
    f"{I}metadata def CandidateKPI {{",
    f"{I}{I}attribute code : String;",
    f"{I}{I}attribute domain : Domain;",
    f"{I}{I}attribute measurementConstruct : String;",
    f"{I}{I}attribute status : RetentionStatus;",
    f"{I}{I}attribute maturity : Operationalization;",
    f"{I}}}",
    f"{I}metadata def DomainExtension {{",
    f"{I}{I}doc /* Construct that extends the reference KPA taxonomy for the domain. */",
    f"{I}{I}attribute fit : TaxonomicFit;",
    f"{I}}}",
    f"{I}metadata def SupportingDiagnosticMetric {{",
    f"{I}{I}doc /* Explains why a system-level KPI behaves as observed; not itself a system-level KPI. */",
    f"{I}}}",
    "",
    f"{I}enum def SourceClass {{",
    f"{I}{I}doc /* Where a KPI input exists according to the FAA concepts of operations (experiment E1).",
    f"{I}{I} * NetworkShared: exchanged across the USS Network or the federated service network during operations.",
    f"{I}{I} * ProviderArchived: retained by USSs, PSUs or operators and available on authorized request.",
    f"{I}{I} * InternallyHeld: exists within one operator or provider, with no sharing or archiving requirement.",
    f"{I}{I} * NotAddressed: no corresponding data element in the concept of operations. */",
    f"{I}{I}enum NetworkShared;",
    f"{I}{I}enum ProviderArchived;",
    f"{I}{I}enum InternallyHeld;",
    f"{I}{I}enum NotAddressed;",
    f"{I}}}",
    f"{I}enum def InputRole {{",
    f"{I}{I}doc /* Principal: the quantity the KPI counts or measures; Supporting: any other input. */",
    f"{I}{I}enum Principal;",
    f"{I}{I}enum Supporting;",
    f"{I}}}",
    f"{I}attribute def KPIInput {{",
    f"{I}{I}doc /* A quantity consumed by a KPI candidate, described in its doc and classified by @DataSource. */",
    f"{I}}}",
    f"{I}metadata def DataSource {{",
    f"{I}{I}doc /* Source class of a data element in the FAA concepts of operations, with the section and printed page. */",
    f"{I}{I}attribute sourceClass : SourceClass;",
    f"{I}{I}attribute conopsRef : String;",
    f"{I}}}",
    f"{I}metadata def KPIInputRole {{",
    f"{I}{I}doc /* Role of an input in a KPI; on a KPIInput attribute, or on a dependency from a KPI to a data-item attribute. */",
    f"{I}{I}attribute role : InputRole;",
    f"{I}}}",
])))

# 2. KPAs da ICAO
cells.append(("ICAO_KPAs", pkg("ICAO_KPAs",
    "The eleven ICAO ATM reference KPAs (ICAO Doc 9854 and Doc 9883), used as the common "
    "performance reference structure. Performance Intents: article 1, Table 1.",
    [], [f"{I}concern def {k} {{ doc /* ICAO reference KPA: {t}. */ }}" for k, t in KPAS])))

# 3. Fronteiras
cells.append(("System_Boundaries", pkg("System_Boundaries",
    "Selected system boundaries (article 1, Sec. 2.4).", [], [
    f"{I}part def UTMSystem {{",
    f"{I}{I}doc /* Based on the FAA UTM ConOps v2.0: traffic-management services, operational coordination,",
    f"{I}{I} * information exchange, service interactions and constraint management that support",
    f"{I}{I} * unmanned operations. Intrinsic aircraft or propulsion characteristics are excluded. */",
    f"{I}}}",
    f"{I}part def AAMSystem {{",
    f"{I}{I}doc /* Based on the FAA UAM ConOps v2.0 and AAM Implementation Plan: an integrated mobility",
    f"{I}{I} * system of systems with aircraft operations, traffic-management interactions, vertiports,",
    f"{I}{I} * supporting infrastructure, energy, digital services, ground access, users and affected",
    f"{I}{I} * communities. UAM is treated as the urban subset of AAM. */",
    f"{I}}}",
])))

# 4. Padroes comuns (propostos para o artigo 2)
cells.append(("KPI_Patterns", pkg("KPI_Patterns",
    "Common calculation patterns shared by UTM and AAM candidates. PROPOSED for article 2; "
    "not defined in article 1.", ["ScalarValues"], [
    f"{I}abstract calc def AccommodationRate {{",
    f"{I}{I}doc /* Accommodated demand over valid demand in a period and volume, in percent. */",
    f"{I}{I}in accommodated : Natural;",
    f"{I}{I}in validDemand : Natural;",
    f"{I}{I}return rate : Real = accommodated / validDemand * 100;",
    f"{I}}}",
    f"{I}abstract calc def TemporalConformanceRate {{",
    f"{I}{I}doc /* Completed operations whose actual time deviates from the planned time by no more",
    f"{I}{I} * than the tolerance, over all completed operations, in percent. */",
    f"{I}{I}in withinTolerance : Natural;",
    f"{I}{I}in completed : Natural;",
    f"{I}{I}in toleranceSeconds : Real;",
    f"{I}{I}return rate : Real = withinTolerance / completed * 100;",
    f"{I}}}",
])))


def objectives(dom, pos, applic, boundary, subj):
    body = []
    for k, t in KPAS:
        body += [
            f"{I}requirement def PO_{k} {{",
            f"{I}{I}doc /* {pos[k]} */",
            f"{I}{I}@KPAApplicability {{ domain = Domain::{dom}; applicability = Applicability::{applic[k]}; }}",
            f"{I}{I}subject {subj} : {boundary};",
            f"{I}{I}frame concern kpa : {k};",
            f"{I}}}",
        ]
    return body


cells.append(("UTM_Objectives", pkg("UTM_Objectives",
    "UTM domain-specific Performance Objectives (article 1, Table 3).",
    ["ICAO_KPAs", "KPI_Taxonomy", "System_Boundaries"],
    objectives("UTM", UTM_PO, UTM_APPLIC, "UTMSystem", "utm"))))
cells.append(("AAM_Objectives", pkg("AAM_Objectives",
    "AAM domain-specific Performance Objectives (article 1, Table 4).",
    ["ICAO_KPAs", "KPI_Taxonomy", "System_Boundaries"],
    objectives("AAM", AAM_PO, AAM_APPLIC, "AAMSystem", "aam"))))


def kpis(dom, rows):
    body = []
    for code, name, title, kpa, mc, st, mat, pat in rows:
        spec = f" :> {pat}" if pat in ("AccommodationRate", "TemporalConformanceRate") else ""
        body.append(f"{I}calc def <'{code}'> {name}{spec} {{")
        if pat == "ENV":
            body.append(f"{I}{I}doc /* {code} -- {title}. Marginal energy effect attributable to UTM-induced operational")
            body.append(f"{I}{I} * deviations relative to a reference condition; not total vehicle energy (article 1). */")
        elif pat in ("AccommodationRate", "TemporalConformanceRate"):
            body.append(f"{I}{I}doc /* {code} -- {title}. Formula inherited from {pat}: PROPOSED for article 2. */")
        else:
            body.append(f"{I}{I}doc /* {code} -- {title}. Operationalization not yet specified. */")
        body.append(f"{I}{I}@CandidateKPI {{")
        body.append(f"{I}{I}{I}code = \"{code}\";")
        body.append(f"{I}{I}{I}domain = Domain::{dom};")
        body.append(f"{I}{I}{I}measurementConstruct = \"{mc}\";")
        body.append(f"{I}{I}{I}status = RetentionStatus::{STATUS[st]};")
        body.append(f"{I}{I}{I}maturity = Operationalization::{mat};")
        body.append(f"{I}{I}}}")
        e1 = E1[code]
        body.append(f"{I}{I}comment principalQuantity /* {e1[2]} */")
        for j, (inp, cls, ev) in enumerate(e1[3], 1):
            role = "Principal" if j == 1 else "Supporting"
            body.append(f"{I}{I}attribute input{j} : KPIInput {{")
            body.append(f"{I}{I}{I}doc /* {inp} */")
            body.append(f"{I}{I}{I}@DataSource {{ sourceClass = SourceClass::{SRC[cls]}; conopsRef = \"{ev}\"; }}")
            body.append(f"{I}{I}{I}@KPIInputRole {{ role = InputRole::{role}; }}")
            body.append(f"{I}{I}}}")
        if e1[5]:
            body.append(f"{I}{I}comment calculabilityNote /* {e1[5]} */")
        if pat == "EXT":
            body.append(f"{I}{I}@DomainExtension {{ fit = TaxonomicFit::Provisional; }}")
        if pat == "ENV":
            body.append(f"{I}{I}in actualEnergy : Real;")
            body.append(f"{I}{I}in referenceEnergy : Real;")
            body.append(f"{I}{I}return penalty : Real = (actualEnergy - referenceEnergy) / referenceEnergy * 100;")
        elif pat not in ("AccommodationRate", "TemporalConformanceRate"):
            body.append(f"{I}{I}return kpiValue : Real;")
        body.append(f"{I}}}")
    return body


cells.append(("UTM_KPIs", pkg("UTM_KPIs",
    "The 14 UTM system-level KPI candidates (article 1, Table 3).",
    ["ScalarValues", "KPI_Taxonomy", "KPI_Patterns"], kpis("UTM", UTM_KPIS))))
cells.append(("AAM_KPIs", pkg("AAM_KPIs",
    "The 17 AAM system-level KPI candidates (article 1, Table 4).",
    ["ScalarValues", "KPI_Taxonomy", "KPI_Patterns"], kpis("AAM", AAM_KPIS))))


def diags(kpi_pkg, kpi, metrics, prefix):
    body = []
    for name, d in metrics:
        body += [
            f"{I}calc def {name} {{",
            f"{I}{I}doc /* {d}. */",
            f"{I}{I}@SupportingDiagnosticMetric;",
            f"{I}{I}return metricValue : Real;",
            f"{I}}}",
        ]
    body.append("")
    for name, _ in metrics:
        body.append(f"{I}dependency {prefix}_{name}_explains from {name} to {kpi_pkg}::{kpi};")
    return body


cells.append(("UTM_Diagnostics", pkg("UTM_Diagnostics",
    "Supporting diagnostic metrics for UTM-GI-01 (article 1, Sec. 4.5).",
    ["ScalarValues", "KPI_Taxonomy"], diags("UTM_KPIs", UTM_DIAG[0], UTM_DIAG[1], "d"))))
cells.append(("AAM_Diagnostics", pkg("AAM_Diagnostics",
    "Supporting diagnostic metrics for AAM-CAP-01 (article 1, Sec. 4.5).",
    ["ScalarValues", "KPI_Taxonomy"], diags("AAM_KPIs", AAM_DIAG[0], AAM_DIAG[1], "d"))))

# Rastreabilidade KPI -> PO, um pacote por dominio
for dom, rows in (("UTM", UTM_KPIS), ("AAM", AAM_KPIS)):
    tb = []
    for code, name, *_rest in rows:
        kpa = _rest[1]
        tag = code.replace("-", "_")
        tb.append(f"{I}dependency t_{tag} from {dom}_KPIs::{name} to {dom}_Objectives::PO_{kpa};")
    cells.append((f"{dom}_Traceability", pkg(f"{dom}_Traceability",
        f"Traceability {dom} KPI -> Performance Objective (the PO frames its KPA concern).", [], tb)))

os.makedirs(OUT, exist_ok=True)
GROUPS = {
    "Common": ["KPI_Taxonomy", "ICAO_KPAs", "System_Boundaries", "KPI_Patterns"],
    "UTM": ["UTM_Objectives", "UTM_KPIs", "UTM_Diagnostics", "UTM_Traceability"],
    "AAM": ["AAM_Objectives", "AAM_KPIs", "AAM_Diagnostics", "AAM_Traceability"],
}
HEAD = {
    "Common": "Shared core: ICAO KPAs, classification metadata, system boundaries and common calculation patterns.",
    "UTM": "UTM domain: 11 Performance Objectives and 14 KPI candidates (article 1, Table 3), anchored in the FAA UTM ConOps v2.0. Requires KPI_Common.sysml.",
    "AAM": "AAM domain (UAM as urban subset): 11 Performance Objectives and 17 KPI candidates (article 1, Table 4), anchored in the FAA UAM ConOps v2.0. Requires KPI_Common.sysml.",
}
cd = dict(cells)
for g, names in GROUPS.items():
    with open(os.path.join(OUT, f"KPI_{g}.sysml"), "w", encoding="utf-8") as f:
        f.write(f"// KPI_{g}.sysml\n// {HEAD[g]}\n// Generated from article 1 and the E1 source classification. Formulas marked PROPOSED are for article 2.\n\n")
        f.write("\n\n".join(cd[n] for n in names) + "\n")
json.dump({"cells": cells, "groups": GROUPS}, open(os.path.join(OUT, "cells.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(UTM_KPIS), len(AAM_KPIS), len(cells))
