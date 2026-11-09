// KPI_UTM.sysml
// UTM domain: 11 Performance Objectives and 14 KPI candidates (article 1, Table 3), anchored in the FAA UTM ConOps v2.0. Requires KPI_Common.sysml.
// Generated from article 1 and the E1 source classification. Formulas marked PROPOSED are for article 2.

package UTM_Objectives {
    doc /* UTM domain-specific Performance Objectives (article 1, Table 3). */
    private import ICAO_KPAs::*;
    private import KPI_Taxonomy::*;
    private import System_Boundaries::*;

    requirement def PO_AccessAndEquity {
        doc /* Promote equitable access to UTM-enabled operations among eligible users. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : AccessAndEquity;
    }
    requirement def PO_Capacity {
        doc /* Accommodate valid operational demand within the available UTM operational environment. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Capacity;
    }
    requirement def PO_CostEffectiveness {
        doc /* Provide UTM services with efficient use of attributable system resources. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : CostEffectiveness;
    }
    requirement def PO_Efficiency {
        doc /* Minimize operational inefficiencies attributable to UTM constraints and decisions. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Efficiency;
    }
    requirement def PO_Environment {
        doc /* Limit environmental burden attributable to UTM-related operational decisions. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::ConditionallyApplicable; }
        subject utm : UTMSystem;
        frame concern kpa : Environment;
    }
    requirement def PO_Flexibility {
        doc /* Maintain operational adaptability and continuity under changing or degraded conditions. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Flexibility;
    }
    requirement def PO_GlobalInteroperability {
        doc /* Enable effective operational interaction and information exchange among UTM actors and services. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : GlobalInteroperability;
    }
    requirement def PO_Participation {
        doc /* Enable meaningful participation of relevant stakeholders in UTM-related processes and decisions. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Participation;
    }
    requirement def PO_Predictability {
        doc /* Provide predictable operational outcomes with respect to planned timing. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Predictability;
    }
    requirement def PO_Safety {
        doc /* Maintain acceptable operational safety for airborne operations and affected third parties. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Safety;
    }
    requirement def PO_Security {
        doc /* Protect UTM operations, services, and information against security compromise. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject utm : UTMSystem;
        frame concern kpa : Security;
    }
}

package UTM_KPIs {
    doc /* The 14 UTM system-level KPI candidates (article 1, Table 3). */
    private import ScalarValues::*;
    private import KPI_Taxonomy::*;
    private import KPI_Patterns::*;

    calc def <'UTM-AE-01'> EquitableAccessGap {
        doc /* UTM-AE-01 -- Equitable Access Gap. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-AE-01";
            domain = Domain::UTM;
            measurementConstruct = "Between-Group Access Disparity";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Accommodation outcome per eligible user group */
        attribute input1 : KPIInput {
            doc /* Outcome of shared operation intents (Accepted state) */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §2.4.4, p. 18; §3.2, p. 39"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Requested demand per user group (plans not shared) */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.4.4, p. 17; §3.2, p. 37"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* User-group attribute of each operator */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM §2.7.3, p. 32 (equity principle only)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* Equity is stated as a principle (no priority scheme), but no grouping or demand record is defined. */
        return kpiValue : Real;
    }
    calc def <'UTM-CAP-01'> DemandAccommodationRate :> AccommodationRate {
        doc /* UTM-CAP-01 -- Demand Accommodation Rate. Formula inherited from AccommodationRate: PROPOSED for article 2. */
        @CandidateKPI {
            code = "UTM-CAP-01";
            domain = Domain::UTM;
            measurementConstruct = "Demand Accommodation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
        comment principalQuantity /* Accepted operation intents */
        attribute input1 : KPIInput {
            doc /* Operation intents shared with the USS Network (Accepted state) */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §2.4.4, p. 18; §3.2, p. 39"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Valid demand, including plans never shared */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.4.4, p. 17; §3.2, p. 37"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Requested time, for the shift window */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §3.2, p. 37 (initial planning information to the USS)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* Plans that cannot be de-conflicted are never shared, so the denominator is invisible to the network. */
    }
    calc def <'UTM-CE-01'> ServiceCostPerManagedOperation {
        doc /* UTM-CE-01 -- UTM Service Cost per Managed Operation. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-CE-01";
            domain = Domain::UTM;
            measurementConstruct = "Unit UTM Service Cost";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Attributable UTM service cost */
        attribute input1 : KPIInput {
            doc /* Cost of USS and FIMS services */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM §1.1, p. 2; §2.2, p. 7 (cost to government only)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Managed operations */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.3.2, p. 11; App. C, p. 64"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-EFF-01'> AttributableOperationalDelay {
        doc /* UTM-EFF-01 -- UTM-Attributable Operational Delay. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-EFF-01";
            domain = Domain::UTM;
            measurementConstruct = "UTM-Attributable Temporal Inefficiency";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Actual operation timing */
        attribute input1 : KPIInput {
            doc /* Actual start and end (4D position tracks) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.7.2, pp. 30-31"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Requested time before de-confliction */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §3.2, p. 37"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Reference (unconstrained) condition */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* Attribution to UTM requires a counterfactual not defined in the ConOps. */
        return kpiValue : Real;
    }
    calc def <'UTM-EFF-02'> InducedTrajectoryExtension {
        doc /* UTM-EFF-02 -- UTM-Induced Trajectory Extension. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-EFF-02";
            domain = Domain::UTM;
            measurementConstruct = "UTM-Attributable Spatial Inefficiency";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Actual flight path length */
        attribute input1 : KPIInput {
            doc /* 4D position tracks and reroute changes to intent */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.7.2, p. 31"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Nominal 4D path before de-confliction */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §3.2, p. 37"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Reference (unconstrained) path */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* As UTM-EFF-01: the reference path is operator-internal or undefined. */
        return kpiValue : Real;
    }
    calc def <'UTM-ENV-01'> InducedEnergyPenalty {
        doc /* UTM-ENV-01 -- UTM-Induced Energy Penalty. Marginal energy effect attributable to UTM-induced operational
         * deviations relative to a reference condition; not total vehicle energy (article 1). */
        @CandidateKPI {
            code = "UTM-ENV-01";
            domain = Domain::UTM;
            measurementConstruct = "UTM-Attributable Marginal Energy Burden";
            status = RetentionStatus::ConditionallyRetained;
            maturity = Operationalization::ConceptualFormulaInArticle1;
        }
        comment principalQuantity /* Actual energy of UTM-affected operations */
        attribute input1 : KPIInput {
            doc /* Endurance or fuel levels (optional report to the USS) */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.7.1, p. 27"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Reference energy */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* Consistent with its conditional retention in article 1. */
        in actualEnergy : Real;
        in referenceEnergy : Real;
        return penalty : Real = (actualEnergy - referenceEnergy) / referenceEnergy * 100;
    }
    calc def <'UTM-FLEX-01'> SuccessfulReplanningRate {
        doc /* UTM-FLEX-01 -- Successful Replanning Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-FLEX-01";
            domain = Domain::UTM;
            measurementConstruct = "Successful Operational Adaptation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Successful in-flight intent updates */
        attribute input1 : KPIInput {
            doc /* In-flight intent updates and reroute changes */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.4.6, p. 19; §2.7.2, p. 31; App. D, p. 65"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Operation outcome after replanning (Closed state) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §3.2, p. 39"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-FLEX-02'> DegradedServiceContinuityRate {
        doc /* UTM-FLEX-02 -- Degraded-Service Continuity Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-FLEX-02";
            domain = Domain::UTM;
            measurementConstruct = "Essential Service Continuity Under Degradation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Operations continued under degradation */
        attribute input1 : KPIInput {
            doc /* Operation outcome (Closed state) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §3.2, p. 39"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Record of USS service degradation events */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM §2.7.2, p. 31 (degradation named as a threat only); App. E, p. 68 (TCL3-7)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-GI-01'> SuccessfulInformationExchangeRate {
        doc /* UTM-GI-01 -- Successful Operational Information Exchange Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-GI-01";
            domain = Domain::UTM;
            measurementConstruct = "Fit-for-Purpose Operational Information Exchange";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Successful USS-USS and USS-FIMS exchanges */
        attribute input1 : KPIInput {
            doc /* Exchange attempts and results (provider system logs) */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.3.2, p. 11; App. C, p. 63 (exchange required, not logged)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Latency, message loss, API success, information age (diagnostics) */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* The exchanges are mandatory, but their success is not recorded as shared or archived data. */
        return kpiValue : Real;
    }
    calc def <'UTM-PART-01'> EffectiveStakeholderParticipationRate {
        doc /* UTM-PART-01 -- Effective Stakeholder Participation Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-PART-01";
            domain = Domain::UTM;
            measurementConstruct = "Effective Stakeholder Participation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Effective participation in UTM processes */
        attribute input1 : KPIInput {
            doc /* Participation records */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM §2.4.2, p. 16; App. A, p. 59 (process described, no data)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-PRED-01'> OperationTimePredictabilityRate :> TemporalConformanceRate {
        doc /* UTM-PRED-01 -- Operation-Time Predictability Rate. Formula inherited from TemporalConformanceRate: PROPOSED for article 2. */
        @CandidateKPI {
            code = "UTM-PRED-01";
            domain = Domain::UTM;
            measurementConstruct = "Temporal Predictability";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
        comment principalQuantity /* Operations starting within tolerance */
        attribute input1 : KPIInput {
            doc /* Planned start: entry time of the first Operation Volume */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §2.7.1, p. 23; §3.2, p. 39"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Actual start: flight data sent to the USS, archived as 4D tracks */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §3.2, p. 39; §2.7.2, p. 31"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        comment calculabilityNote /* The tolerance value is not specified in the ConOps. */
    }
    calc def <'UTM-SAF-01'> SeparationSafetyEventRate {
        doc /* UTM-SAF-01 -- Separation-Safety Event Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-SAF-01";
            domain = Domain::UTM;
            measurementConstruct = "Separation-Related Safety Event Frequency";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Separation-related safety events */
        attribute input1 : KPIInput {
            doc /* Non-Conforming and Rogue states, off-nominal event records */
            @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §3.2, p. 39 (fn. 33); §2.7.2, p. 31"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Incident reports to the FAA via FIMS */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.7.1, p. 28; App. E, p. 68 (TCL4-5)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* Exposure (flight hours from 4D tracks) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.7.2, p. 31"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input4 : KPIInput {
            doc /* Event taxonomy and severity (e.g., loss of well clear) */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "-"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-SAF-02'> InfluencedGroundThirdPartyRisk {
        doc /* UTM-SAF-02 -- UTM-Influenced Ground Third-Party Risk. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-SAF-02";
            domain = Domain::UTM;
            measurementConstruct = "UTM-Influenced Ground Third-Party Risk";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Ground risk exposure */
        attribute input1 : KPIInput {
            doc /* Population and ground exposure data */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM App. D, p. 66 (mapping of ground constraints only)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Risk model */
            @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.4.6, p. 19 (fn. 19: USS-integrated risk assessment)"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        attribute input3 : KPIInput {
            doc /* 4D position tracks */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §2.7.2, p. 31"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
    calc def <'UTM-SEC-01'> SecurityCompromiseRate {
        doc /* UTM-SEC-01 -- Security Compromise Rate. Operationalization not yet specified. */
        @CandidateKPI {
            code = "UTM-SEC-01";
            domain = Domain::UTM;
            measurementConstruct = "Operational Security Compromise Frequency";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::Pending;
        }
        comment principalQuantity /* Security compromises */
        attribute input1 : KPIInput {
            doc /* Record of cyber or security incidents */
            @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "UTM §2.7.2, pp. 29-31 (threats and IATF policies, no record)"; }
            @KPIInputRole { role = InputRole::Principal; }
        }
        attribute input2 : KPIInput {
            doc /* Exposure (operations) */
            @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM App. C, p. 64"; }
            @KPIInputRole { role = InputRole::Supporting; }
        }
        return kpiValue : Real;
    }
}

package UTM_Diagnostics {
    doc /* Supporting diagnostic metrics for UTM-GI-01 (article 1, Sec. 4.5). */
    private import ScalarValues::*;
    private import KPI_Taxonomy::*;

    calc def ExchangeLatency {
        doc /* Latency of operational information exchange. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def MessageLoss {
        doc /* Message loss. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def APICallSuccess {
        doc /* API call success. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def InformationAge {
        doc /* Age of operational information. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def InformationConsistency {
        doc /* Consistency of shared operational information. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }

    dependency d_ExchangeLatency_explains from ExchangeLatency to UTM_KPIs::SuccessfulInformationExchangeRate;
    dependency d_MessageLoss_explains from MessageLoss to UTM_KPIs::SuccessfulInformationExchangeRate;
    dependency d_APICallSuccess_explains from APICallSuccess to UTM_KPIs::SuccessfulInformationExchangeRate;
    dependency d_InformationAge_explains from InformationAge to UTM_KPIs::SuccessfulInformationExchangeRate;
    dependency d_InformationConsistency_explains from InformationConsistency to UTM_KPIs::SuccessfulInformationExchangeRate;
}

package UTM_Traceability {
    doc /* Traceability UTM KPI -> Performance Objective (the PO frames its KPA concern). */

    dependency t_UTM_AE_01 from UTM_KPIs::EquitableAccessGap to UTM_Objectives::PO_AccessAndEquity;
    dependency t_UTM_CAP_01 from UTM_KPIs::DemandAccommodationRate to UTM_Objectives::PO_Capacity;
    dependency t_UTM_CE_01 from UTM_KPIs::ServiceCostPerManagedOperation to UTM_Objectives::PO_CostEffectiveness;
    dependency t_UTM_EFF_01 from UTM_KPIs::AttributableOperationalDelay to UTM_Objectives::PO_Efficiency;
    dependency t_UTM_EFF_02 from UTM_KPIs::InducedTrajectoryExtension to UTM_Objectives::PO_Efficiency;
    dependency t_UTM_ENV_01 from UTM_KPIs::InducedEnergyPenalty to UTM_Objectives::PO_Environment;
    dependency t_UTM_FLEX_01 from UTM_KPIs::SuccessfulReplanningRate to UTM_Objectives::PO_Flexibility;
    dependency t_UTM_FLEX_02 from UTM_KPIs::DegradedServiceContinuityRate to UTM_Objectives::PO_Flexibility;
    dependency t_UTM_GI_01 from UTM_KPIs::SuccessfulInformationExchangeRate to UTM_Objectives::PO_GlobalInteroperability;
    dependency t_UTM_PART_01 from UTM_KPIs::EffectiveStakeholderParticipationRate to UTM_Objectives::PO_Participation;
    dependency t_UTM_PRED_01 from UTM_KPIs::OperationTimePredictabilityRate to UTM_Objectives::PO_Predictability;
    dependency t_UTM_SAF_01 from UTM_KPIs::SeparationSafetyEventRate to UTM_Objectives::PO_Safety;
    dependency t_UTM_SAF_02 from UTM_KPIs::InfluencedGroundThirdPartyRisk to UTM_Objectives::PO_Safety;
    dependency t_UTM_SEC_01 from UTM_KPIs::SecurityCompromiseRate to UTM_Objectives::PO_Security;
}
