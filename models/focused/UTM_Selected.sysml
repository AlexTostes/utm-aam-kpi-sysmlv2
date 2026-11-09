package UTM_Selected {
    doc /* Focused model for the two UTM KPIs prioritized for synthetic data in article 2:
     * UTM-CAP-01 (Demand Accommodation Rate) and UTM-PRED-01 (Operation-Time Predictability Rate).
     * Anchored in the FAA UTM ConOps v2.0. Only the elements needed to compute the two KPIs are
     * modeled (minimum-sufficiency criterion). Formulas and parameters are PROPOSED for article 2. */
    private import ScalarValues::*;
    private import ICAO_KPAs::*;
    private import KPI_Taxonomy::*;
    private import KPI_Patterns::*;
    private import System_Boundaries::*;

    // ---------- Architecture (FAA UTM ConOps v2.0, Sec. 2.3) ----------

    part def Operator {
        doc /* Operator: plans the operation and shares operation intent, via its USS
         * (UTM ConOps Sec. 2.3.1, p. 9; Sec. 2.4.4, pp. 17-18). */
    }
    part def USS {
        doc /* UAS Service Supplier: communications bridge between federated actors, supports strategic
         * de-confliction and conformance monitoring, and archives operations data for analytics,
         * regulatory and accountability purposes (UTM ConOps Sec. 2.3.2, p. 11; App. C, pp. 63-64). */
        ref item receivedIntents : OperationIntent[0..*];
        ref item archivedRecords : OperationRecord[0..*];
    }
    part def USSNetwork {
        doc /* USS Network: USSs connected to each other, sharing operation intent and airspace
         * constraint information (UTM ConOps Sec. 2.3.2, p. 11). */
    }
    part def FIMS {
        doc /* Flight Information Management System: interface for data exchange between FAA systems and
         * UTM participants; also the access point for post-hoc archived data (UTM ConOps Sec. 2.3.2, p. 12). */
    }
    part def UTMEnvironment :> UTMSystem {
        doc /* Instance of the selected UTM boundary used for the synthetic study. */
        part operators : Operator[1..*];
        part ussProviders : USS[2..*];
        part network : USSNetwork[1];
        part fims : FIMS[1];
    }

    // ---------- Data items consumed by the KPIs ----------

    enum def IntentOutcome {
        doc /* Planning outcome used by the synthetic study. Accepted and Withdrawn follow the ConOps
         * (Sec. 3.2, p. 39; Sec. 2.7.3, p. 33). The Rejected outcomes are not ConOps states: a plan that
         * cannot be de-conflicted is simply not shared, so these outcomes are internally held. */
        enum Accepted;
        enum RejectedConflict;
        enum RejectedConstraint;
        enum RejectedInvalid;
        enum Withdrawn;
    }
    item def OperationIntent {
        doc /* Operation intent: Operation Volume segments with entry and exit times (UTM ConOps Sec. 2.7.1,
         * p. 23), shared with the USS Network once planning is complete; the operation is then in the
         * Accepted state (Sec. 3.2, p. 39). requestedStart comes from the initial planning information
         * the operator gives its USS (p. 37) and is internally held: the ConOps defines no sharing or
         * archiving of it. Times in seconds from the start of the measurement period. */
        attribute intentId : String;
        attribute isValid : Boolean { @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §2.4.4, p. 17; §3.2, p. 37"; } }
        attribute outcome : IntentOutcome { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §2.4.4, p. 18; §3.2, p. 39"; } }
        attribute requestedStart : Real { @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UTM §3.2, p. 37"; } }
        attribute plannedStart : Real { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UTM §2.7.1, p. 23; §3.2, p. 39"; } }
        attribute plannedEnd : Real;
    }
    item def OperationRecord {
        doc /* Archived record of a completed operation: actual times from the flight data sent to the
         * USS and archived as 4D position tracks (UTM ConOps Sec. 3.2, p. 39; Sec. 2.7.2, p. 31). */
        attribute intentId : String;
        attribute actualStart : Real { @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UTM §3.2, p. 39; §2.7.2, p. 31"; } }
        attribute actualEnd : Real;
    }

    // ---------- Measurement parameters (open decisions, section 3.4 of the proposal) ----------

    attribute def MeasurementParameters {
        doc /* periodSeconds = aggregation period T; toleranceSeconds = tau for UTM-PRED-01;
         * shiftWindowSeconds = Delta, the negotiated shift still counted as accommodated in UTM-CAP-01. */
        attribute periodSeconds : Real;
        attribute toleranceSeconds : Real;
        attribute shiftWindowSeconds : Real;
    }

    // ---------- Performance Objectives (article 1, Table 3) ----------

    requirement def PO_Capacity {
        doc /* Accommodate valid operational demand within the available UTM operational environment. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject env : UTMEnvironment;
        frame concern kpa : Capacity;
    }
    requirement def PO_Predictability {
        doc /* Provide predictable operational outcomes with respect to planned timing. */
        @KPAApplicability { domain = Domain::UTM; applicability = Applicability::Applicable; }
        subject env : UTMEnvironment;
        frame concern kpa : Predictability;
    }

    // ---------- KPI candidates ----------

    calc def <'UTM-CAP-01'> DemandAccommodationRate :> AccommodationRate {
        doc /* accommodated = valid intents accepted by the USS (outcome Accepted, or Withdrawn after
         * acceptance) with plannedStart - requestedStart no greater than Delta; validDemand = valid
         * intents submitted in the period. PROPOSED. */
        @CandidateKPI {
            code = "UTM-CAP-01";
            domain = Domain::UTM;
            measurementConstruct = "Demand Accommodation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
    }
    calc def <'UTM-PRED-01'> OperationTimePredictabilityRate :> TemporalConformanceRate {
        doc /* withinTolerance = completed operations with |actualStart - plannedStart| no greater than tau;
         * completed = operations with an archived record in the period. PROPOSED. */
        @CandidateKPI {
            code = "UTM-PRED-01";
            domain = Domain::UTM;
            measurementConstruct = "Temporal Predictability";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
    }

    // ---------- Supporting diagnostic metrics ----------

    calc def RejectionsByCause {
        doc /* Share of rejected intents per cause (conflict, constraint). Diagnostic of UTM-CAP-01. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def IntentDensity {
        doc /* Valid intents per volume and period. Diagnostic of UTM-CAP-01. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }
    calc def StartDeviationP95 {
        doc /* 95th percentile of |actualStart - plannedStart|, in seconds. Diagnostic of UTM-PRED-01. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }

    // ---------- Traceability ----------

    dependency cap_measures_po from DemandAccommodationRate to PO_Capacity;
    dependency pred_measures_po from OperationTimePredictabilityRate to PO_Predictability;

    dependency cap_uses_validity from DemandAccommodationRate to OperationIntent::isValid { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_outcome from DemandAccommodationRate to OperationIntent::outcome { @KPIInputRole { role = InputRole::Principal; } }
    dependency cap_uses_requested from DemandAccommodationRate to OperationIntent::requestedStart { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_planned from DemandAccommodationRate to OperationIntent::plannedStart { @KPIInputRole { role = InputRole::Supporting; } }
    dependency pred_uses_planned from OperationTimePredictabilityRate to OperationIntent::plannedStart { @KPIInputRole { role = InputRole::Principal; } }
    dependency pred_uses_actual from OperationTimePredictabilityRate to OperationRecord::actualStart { @KPIInputRole { role = InputRole::Supporting; } }

    dependency rejections_explains from RejectionsByCause to DemandAccommodationRate;
    dependency density_explains from IntentDensity to DemandAccommodationRate;
    dependency deviation_explains from StartDeviationP95 to OperationTimePredictabilityRate;

    // ---------- KPI targets as verifiable requirements ----------

    requirement def CapacityTarget :> PO_Capacity {
        doc /* Refines PO_Capacity into a verifiable statement on UTM-CAP-01: the measured value shall be at
         * least the target. Target values are illustrative assumptions of the synthetic study. */
        attribute measured : Real;
        attribute target : Real;
        require constraint { measured >= target }
    }
    requirement def PredictabilityTarget :> PO_Predictability {
        doc /* Refines PO_Predictability into a verifiable statement on UTM-PRED-01. */
        attribute measured : Real;
        attribute target : Real;
        require constraint { measured >= target }
    }
    dependency capTarget_on_kpi from CapacityTarget to DemandAccommodationRate;
    dependency predTarget_on_kpi from PredictabilityTarget to OperationTimePredictabilityRate;

    // ---------- Synthetic study ----------

    part def SyntheticScenario {
        doc /* Configuration of one synthetic run (experiments E2 to E4 of the proposal). */
        attribute demandPerHour : Real;
        attribute ussCount : Natural;
        attribute constraintActive : Boolean;
        attribute messageFailureProbability : Real;
        attribute startDeviationSigmaSeconds : Real;
        attribute params : MeasurementParameters;
    }
    analysis def CapacityPredictabilityRun {
        doc /* One synthetic run: the generator produces intents and records for the scenario; the
         * counts below are taken from them and both KPIs are evaluated. */
        subject scenario : SyntheticScenario;
        objective {
            doc /* Observe UTM-CAP-01 and UTM-PRED-01 under the scenario configuration. */
        }
        in nAccommodated : Natural;
        in nValid : Natural;
        in nWithinTolerance : Natural;
        in nCompleted : Natural;
        out capResult : Real = DemandAccommodationRate(nAccommodated, nValid);
        out predResult : Real = OperationTimePredictabilityRate(nWithinTolerance, nCompleted, scenario.params.toleranceSeconds);
    }

    // ---------- Base case: analysis result bound to the targets ----------

    part baseCase : UTMEnvironment;
    analysis baseRun : CapacityPredictabilityRun;
    requirement baseCaseCapacity : CapacityTarget {
        attribute :>> measured = baseRun.capResult;
        attribute :>> target = 75.0;
    }
    requirement baseCasePredictability : PredictabilityTarget {
        attribute :>> measured = baseRun.predResult;
        attribute :>> target = 80.0;
    }
    satisfy baseCaseCapacity by baseCase;
    satisfy baseCasePredictability by baseCase;
}
