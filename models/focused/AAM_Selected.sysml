package AAM_Selected {
    doc /* Focused model for the two AAM KPIs prioritized for synthetic data in article 2:
     * AAM-CAP-01 (Integrated Demand Accommodation Rate) and AAM-PRED-01 (Operational Punctuality).
     * Evaluated within the scope of the FAA UAM ConOps v2.0 (UAM as the urban subset of AAM).
     * Only the elements needed to compute the two KPIs are modeled (minimum-sufficiency criterion).
     * Formulas and parameters are PROPOSED for article 2. */
    private import ScalarValues::*;
    private import ICAO_KPAs::*;
    private import KPI_Taxonomy::*;
    private import KPI_Patterns::*;
    private import System_Boundaries::*;

    // ---------- Architecture (FAA UAM ConOps v2.0, Sec. 4.3 and Sec. 5) ----------

    part def UAMOperator {
        doc /* UAM operator: conducts scheduled or on-demand operations from customer requests and submits
         * the desired UAM Operational Intent to its PSU (UAM ConOps Sec. 4.3.2, p. 13). */
        ref item flightRecords : FlightRecord[0..*];
    }
    part def PSU {
        doc /* Provider of Services for UAM: confirms that a submitted UAM Operational Intent is complete and
         * strategically deconflicted, shares it with the federated service network, and archives
         * operational data (UAM ConOps Sec. 4.3.4, p. 14). */
        ref item receivedRequests : TripRequest[0..*];
    }
    part def FederatedServiceNetwork {
        doc /* Federated service network: the collection of connected PSUs sharing subscriber, FAA and
         * supplemental data (UAM ConOps Sec. 4.3.5, p. 15). */
    }
    part def FAAIndustryDataExchange {
        doc /* FAA-Industry Data Exchange Protocol: interface through which the FAA requests UAM operational
         * data on demand and sends FAA information to the federated service network (UAM ConOps
         * Sec. 4.3.1.3, p. 12; Sec. 5, p. 23). The UAM ConOps does not use the term FIMS. */
    }
    part def Vertiport {
        doc /* UAM vertiport: provides current and future resource availability (e.g., open/closed, pad
         * availability) to the network (UAM ConOps Sec. 4.3.7, p. 15). Chargers are an assumption of the
         * synthetic study; charging is not addressed in the ConOps. */
        attribute padCount : Natural { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.7, p. 15"; } }
        attribute chargerCount : Natural { @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "- (not addressed)"; } }
    }
    part def UAMAircraft {
        attribute available : Boolean { @DataSource { sourceClass = SourceClass::NotAddressed; conopsRef = "- (not addressed)"; } }
    }
    part def UAMCorridor {
        doc /* UAM Corridor; availability (open/closed) is set by ATC (UAM ConOps Sec. 4.3.1.2, p. 12). */
        attribute open : Boolean { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.1, p. 12; §4.4, p. 17"; } }
    }
    part def AAMNetwork :> AAMSystem {
        doc /* Instance of the selected AAM boundary used for the synthetic study. */
        part operators : UAMOperator[1..*];
        part psuProviders : PSU[1..*];
        part network : FederatedServiceNetwork[1];
        part dataExchange : FAAIndustryDataExchange[1];
        part vertiports : Vertiport[2..*];
        part fleet : UAMAircraft[1..*];
        part corridors : UAMCorridor[1..*];
    }

    // ---------- Data items consumed by the KPIs ----------

    enum def ServiceOutcome {
        doc /* Confirmed: the PSU confirmed the UAM Operational Intent (UAM ConOps Sec. 4.3.4, p. 14).
         * DeniedNoPad and DeniedAirspace map to vertiport resources and airspace or corridor constraints
         * named in the ConOps; DeniedNoCharge and DeniedNoAircraft are operator-internal causes that the
         * ConOps does not address. */
        enum Confirmed;
        enum DeniedNoPad;
        enum DeniedNoCharge;
        enum DeniedNoAircraft;
        enum DeniedAirspace;
        enum DeniedInvalid;
    }
    item def TripRequest {
        doc /* Customer request for a trip between two vertiports, received by the UAM operator (UAM ConOps
         * Sec. 4.3.2, p. 13; Sec. 6.1.1, p. 25). scheduledDeparture is the departure time of the
         * confirmed UAM Operational Intent (Sec. 3.2, p. 8); it is set only for confirmed requests. Internally held by the operator: requests that are not
         * served never become UAM Operational Intents. Times in seconds from the start of the period. */
        attribute requestId : String;
        attribute isValid : Boolean { @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UAM §4.3.2, p. 13; §6.1.1, p. 25"; } }
        attribute outcome : ServiceOutcome { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §4.3.4, p. 14 (items 3-4)"; } }
        attribute requestedDeparture : Real { @DataSource { sourceClass = SourceClass::InternallyHeld; conopsRef = "UAM §4.3.2, p. 13; §6.1.1, p. 25"; } }
        attribute scheduledDeparture : Real { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §3.2, p. 8"; } }
    }
    item def FlightRecord {
        doc /* Record of a completed flight. Scheduled times are the key operational event times of the
         * confirmed UAM Operational Intent (UAM ConOps Sec. 3.2, p. 8); actual times come from operational
         * data archived by the PSU (Sec. 4.3.4, p. 14, item 8; Sec. 6.1.3, p. 26). */
        attribute requestId : String;
        attribute scheduledDeparture : Real;
        attribute scheduledArrival : Real { @DataSource { sourceClass = SourceClass::NetworkShared; conopsRef = "UAM §3.2, p. 8"; } }
        attribute actualDeparture : Real;
        attribute actualArrival : Real { @DataSource { sourceClass = SourceClass::ProviderArchived; conopsRef = "UAM §6.1.2, p. 25; §4.3.4, p. 14 (item 8)"; } }
    }

    // ---------- Measurement parameters (open decisions, section 3.4 of the proposal) ----------

    attribute def MeasurementParameters {
        doc /* periodSeconds = aggregation period T; toleranceSeconds = tau for AAM-PRED-01, applied to
         * arrival time; shiftWindowSeconds = Delta, the departure shift still counted as served. */
        attribute periodSeconds : Real;
        attribute toleranceSeconds : Real;
        attribute shiftWindowSeconds : Real;
    }

    // ---------- Performance Objectives (article 1, Table 4) ----------

    requirement def PO_Capacity {
        doc /* Accommodate transportation demand within the integrated AAM operational system. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject net : AAMNetwork;
        frame concern kpa : Capacity;
    }
    requirement def PO_Predictability {
        doc /* Provide predictable operational outcomes with respect to planned timing. */
        @KPAApplicability { domain = Domain::AAM; applicability = Applicability::Applicable; }
        subject net : AAMNetwork;
        frame concern kpa : Predictability;
    }

    // ---------- KPI candidates ----------

    calc def <'AAM-CAP-01'> IntegratedDemandAccommodationRate :> AccommodationRate {
        doc /* accommodated = valid requests with outcome Confirmed (pad, charge, aircraft and corridor all
         * available) and scheduledDeparture - requestedDeparture no greater than Delta; validDemand =
         * valid requests in the period. PROPOSED. */
        @CandidateKPI {
            code = "AAM-CAP-01";
            domain = Domain::AAM;
            measurementConstruct = "Integrated Demand Accommodation";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
    }
    calc def <'AAM-PRED-01'> OperationalPunctuality :> TemporalConformanceRate {
        doc /* withinTolerance = completed flights with |actualArrival - scheduledArrival| no greater
         * than tau; completed = flights with a record in the period. PROPOSED. */
        @CandidateKPI {
            code = "AAM-PRED-01";
            domain = Domain::AAM;
            measurementConstruct = "Temporal Predictability";
            status = RetentionStatus::ProvisionallyRetained;
            maturity = Operationalization::ProposedInThisStudy;
        }
    }

    // ---------- Supporting diagnostic metrics (AAM-CAP-01: article 1, Sec. 4.5) ----------

    calc def VertiportThroughput { doc /* Diagnostic of AAM-CAP-01. */ @SupportingDiagnosticMetric; return metricValue : Real; }
    calc def PadUtilization { doc /* Diagnostic of AAM-CAP-01. */ @SupportingDiagnosticMetric; return metricValue : Real; }
    calc def ChargingAvailability { doc /* Diagnostic of AAM-CAP-01. */ @SupportingDiagnosticMetric; return metricValue : Real; }
    calc def AirspaceConstraints { doc /* Diagnostic of AAM-CAP-01. */ @SupportingDiagnosticMetric; return metricValue : Real; }
    calc def FleetAvailability { doc /* Diagnostic of AAM-CAP-01. */ @SupportingDiagnosticMetric; return metricValue : Real; }
    calc def DelayByCause {
        doc /* Share of late arrivals per cause (charging wait, pad occupancy, corridor restriction).
         * Diagnostic of AAM-PRED-01; proposed for article 2. */
        @SupportingDiagnosticMetric;
        return metricValue : Real;
    }

    // ---------- Traceability ----------

    dependency cap_measures_po from IntegratedDemandAccommodationRate to PO_Capacity;
    dependency pred_measures_po from OperationalPunctuality to PO_Predictability;

    dependency cap_uses_validity from IntegratedDemandAccommodationRate to TripRequest::isValid { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_outcome from IntegratedDemandAccommodationRate to TripRequest::outcome { @KPIInputRole { role = InputRole::Principal; } }
    dependency cap_uses_requested from IntegratedDemandAccommodationRate to TripRequest::requestedDeparture { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_scheduled from IntegratedDemandAccommodationRate to TripRequest::scheduledDeparture { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_pads from IntegratedDemandAccommodationRate to Vertiport::padCount { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_chargers from IntegratedDemandAccommodationRate to Vertiport::chargerCount { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_fleet from IntegratedDemandAccommodationRate to UAMAircraft::available { @KPIInputRole { role = InputRole::Supporting; } }
    dependency cap_uses_corridor from IntegratedDemandAccommodationRate to UAMCorridor::open { @KPIInputRole { role = InputRole::Supporting; } }
    dependency pred_uses_scheduled from OperationalPunctuality to FlightRecord::scheduledArrival { @KPIInputRole { role = InputRole::Principal; } }
    dependency pred_uses_actual from OperationalPunctuality to FlightRecord::actualArrival { @KPIInputRole { role = InputRole::Supporting; } }

    dependency throughput_explains from VertiportThroughput to IntegratedDemandAccommodationRate;
    dependency pads_explains from PadUtilization to IntegratedDemandAccommodationRate;
    dependency charging_explains from ChargingAvailability to IntegratedDemandAccommodationRate;
    dependency airspace_explains from AirspaceConstraints to IntegratedDemandAccommodationRate;
    dependency fleet_explains from FleetAvailability to IntegratedDemandAccommodationRate;
    dependency delay_explains from DelayByCause to OperationalPunctuality;

    // ---------- KPI targets as verifiable requirements ----------

    requirement def CapacityTarget :> PO_Capacity {
        doc /* Refines PO_Capacity into a verifiable statement on AAM-CAP-01: the measured value shall be at
         * least the target. Target values are illustrative assumptions of the synthetic study. */
        attribute measured : Real;
        attribute target : Real;
        require constraint { measured >= target }
    }
    requirement def PredictabilityTarget :> PO_Predictability {
        doc /* Refines PO_Predictability into a verifiable statement on AAM-PRED-01. */
        attribute measured : Real;
        attribute target : Real;
        require constraint { measured >= target }
    }
    dependency capTarget_on_kpi from CapacityTarget to IntegratedDemandAccommodationRate;
    dependency predTarget_on_kpi from PredictabilityTarget to OperationalPunctuality;

    // ---------- Synthetic study ----------

    part def SyntheticScenario {
        doc /* Configuration of one synthetic run (experiments E2 to E4 of the proposal). */
        attribute vertiportCount : Natural;
        attribute padsPerVertiport : Natural;
        attribute chargersPerVertiport : Natural;
        attribute fleetSize : Natural;
        attribute peakDemandPerHour : Real;
        attribute turnaroundSeconds : Real;
        attribute chargingSeconds : Real;
        attribute corridorClosureProbability : Real;
        attribute params : MeasurementParameters;
    }
    analysis def CapacityPredictabilityRun {
        doc /* One synthetic run: the generator produces requests and flight records for the scenario;
         * the counts below are taken from them and both KPIs are evaluated. */
        subject scenario : SyntheticScenario;
        objective {
            doc /* Observe AAM-CAP-01 and AAM-PRED-01 under the scenario configuration. */
        }
        in nConfirmed : Natural;
        in nValid : Natural;
        in nWithinTolerance : Natural;
        in nCompleted : Natural;
        out capResult : Real = IntegratedDemandAccommodationRate(nConfirmed, nValid);
        out predResult : Real = OperationalPunctuality(nWithinTolerance, nCompleted, scenario.params.toleranceSeconds);
    }

    // ---------- Base case: analysis result bound to the targets ----------

    part baseCase : AAMNetwork;
    analysis baseRun : CapacityPredictabilityRun;
    requirement baseCaseCapacity : CapacityTarget {
        attribute :>> measured = baseRun.capResult;
        attribute :>> target = 80.0;
    }
    requirement baseCasePredictability : PredictabilityTarget {
        attribute :>> measured = baseRun.predResult;
        attribute :>> target = 90.0;
    }
    satisfy baseCaseCapacity by baseCase;
    satisfy baseCasePredictability by baseCase;
}
