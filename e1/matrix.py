"""E1 calculability matrix: data inputs of the 31 KPI candidates against the FAA ConOps.

Source classes (data element as described in the ConOps):
  NS  network-shared: exchanged across the USS Network / federated service network during operations
  PA  provider-archived: retained by USSs/PSUs (or operators) and available on authorized request;
      a system-level value requires aggregation across providers
  IH  internally held: exists within an operator or a single provider, with no sharing or archiving
      requirement in the ConOps
  NA  not addressed: no corresponding data element in the ConOps (external source or new data requirement)

Calculability (rule applied uniformly):
  C1  every input is NS or PA
  C2  the principal quantity is NS or PA, but at least one other input is IH or NA
  C3  the principal quantity is IH or NA

Inputs are the minimal quantities implied by each Measurement Construct (author-derived; article 1
defines a formula only for UTM-ENV-01). Citations: section and printed page of FAA UTM ConOps v2.0
(2020) and FAA UAM ConOps v2.0 (2023).
"""

# (code, name, principal quantity, [(input, class, evidence)], calculability, note)
UTM = [
 ("UTM-AE-01", "Equitable Access Gap", "Accommodation outcome per eligible user group", [
   ("Outcome of shared operation intents (Accepted state)", "NS", "UTM §2.4.4, p. 18; §3.2, p. 39"),
   ("Requested demand per user group (plans not shared)", "IH", "UTM §2.4.4, p. 17; §3.2, p. 37"),
   ("User-group attribute of each operator", "NA", "UTM §2.7.3, p. 32 (equity principle only)")],
  "C2", "Equity is stated as a principle (no priority scheme), but no grouping or demand record is defined."),
 ("UTM-CAP-01", "Demand Accommodation Rate", "Accepted operation intents", [
   ("Operation intents shared with the USS Network (Accepted state)", "NS", "UTM §2.4.4, p. 18; §3.2, p. 39"),
   ("Valid demand, including plans never shared", "IH", "UTM §2.4.4, p. 17; §3.2, p. 37"),
   ("Requested time, for the shift window", "IH", "UTM §3.2, p. 37 (initial planning information to the USS)")],
  "C2", "Plans that cannot be de-conflicted are never shared, so the denominator is invisible to the network."),
 ("UTM-CE-01", "UTM Service Cost per Managed Operation", "Attributable UTM service cost", [
   ("Cost of USS and FIMS services", "NA", "UTM §1.1, p. 2; §2.2, p. 7 (cost to government only)"),
   ("Managed operations", "PA", "UTM §2.3.2, p. 11; App. C, p. 64")],
  "C3", ""),
 ("UTM-EFF-01", "UTM-Attributable Operational Delay", "Actual operation timing", [
   ("Actual start and end (4D position tracks)", "PA", "UTM §2.7.2, pp. 30-31"),
   ("Requested time before de-confliction", "IH", "UTM §3.2, p. 37"),
   ("Reference (unconstrained) condition", "NA", "-")],
  "C2", "Attribution to UTM requires a counterfactual not defined in the ConOps."),
 ("UTM-EFF-02", "UTM-Induced Trajectory Extension", "Actual flight path length", [
   ("4D position tracks and reroute changes to intent", "PA", "UTM §2.7.2, p. 31"),
   ("Nominal 4D path before de-confliction", "IH", "UTM §3.2, p. 37"),
   ("Reference (unconstrained) path", "NA", "-")],
  "C2", "As UTM-EFF-01: the reference path is operator-internal or undefined."),
 ("UTM-ENV-01", "UTM-Induced Energy Penalty", "Actual energy of UTM-affected operations", [
   ("Endurance or fuel levels (optional report to the USS)", "IH", "UTM §2.7.1, p. 27"),
   ("Reference energy", "NA", "-")],
  "C3", "Consistent with its conditional retention in article 1."),
 ("UTM-FLEX-01", "Successful Replanning Rate", "Successful in-flight intent updates", [
   ("In-flight intent updates and reroute changes", "PA", "UTM §2.4.6, p. 19; §2.7.2, p. 31; App. D, p. 65"),
   ("Operation outcome after replanning (Closed state)", "PA", "UTM §3.2, p. 39")],
  "C1", ""),
 ("UTM-FLEX-02", "Degraded-Service Continuity Rate", "Operations continued under degradation", [
   ("Operation outcome (Closed state)", "PA", "UTM §3.2, p. 39"),
   ("Record of USS service degradation events", "NA", "UTM §2.7.2, p. 31 (degradation named as a threat only); App. E, p. 68 (TCL3-7)")],
  "C2", ""),
 ("UTM-GI-01", "Successful Operational Information Exchange Rate", "Successful USS-USS and USS-FIMS exchanges", [
   ("Exchange attempts and results (provider system logs)", "IH", "UTM §2.3.2, p. 11; App. C, p. 63 (exchange required, not logged)"),
   ("Latency, message loss, API success, information age (diagnostics)", "IH", "-")],
  "C3", "The exchanges are mandatory, but their success is not recorded as shared or archived data."),
 ("UTM-PART-01", "Effective Stakeholder Participation Rate", "Effective participation in UTM processes", [
   ("Participation records", "NA", "UTM §2.4.2, p. 16; App. A, p. 59 (process described, no data)")],
  "C3", ""),
 ("UTM-PRED-01", "Operation-Time Predictability Rate", "Operations starting within tolerance", [
   ("Planned start: entry time of the first Operation Volume", "NS", "UTM §2.7.1, p. 23; §3.2, p. 39"),
   ("Actual start: flight data sent to the USS, archived as 4D tracks", "PA", "UTM §3.2, p. 39; §2.7.2, p. 31")],
  "C1", "The tolerance value is not specified in the ConOps."),
 ("UTM-SAF-01", "Separation-Safety Event Rate", "Separation-related safety events", [
   ("Non-Conforming and Rogue states, off-nominal event records", "NS", "UTM §3.2, p. 39 (fn. 33); §2.7.2, p. 31"),
   ("Incident reports to the FAA via FIMS", "PA", "UTM §2.7.1, p. 28; App. E, p. 68 (TCL4-5)"),
   ("Exposure (flight hours from 4D tracks)", "PA", "UTM §2.7.2, p. 31"),
   ("Event taxonomy and severity (e.g., loss of well clear)", "NA", "-")],
  "C2", ""),
 ("UTM-SAF-02", "UTM-Influenced Ground Third-Party Risk", "Ground risk exposure", [
   ("Population and ground exposure data", "NA", "UTM App. D, p. 66 (mapping of ground constraints only)"),
   ("Risk model", "IH", "UTM §2.4.6, p. 19 (fn. 19: USS-integrated risk assessment)"),
   ("4D position tracks", "PA", "UTM §2.7.2, p. 31")],
  "C3", ""),
 ("UTM-SEC-01", "Security Compromise Rate", "Security compromises", [
   ("Record of cyber or security incidents", "NA", "UTM §2.7.2, pp. 29-31 (threats and IATF policies, no record)"),
   ("Exposure (operations)", "PA", "UTM App. C, p. 64")],
  "C3", ""),
]

AAM = [
 ("AAM-AE-01", "Population Service Accessibility", "Population within access of the service", [
   ("Population and ground-access data", "NA", "UAM §1.2.3, p. 2 (transportation equity as planning intent)"),
   ("Vertiport locations and corridor definitions", "NS", "UAM §4.3.1, p. 12; §4.3.7, p. 15")],
  "C3", ""),
 ("AAM-AE-02", "Affordability Burden Ratio", "Fare relative to user income", [
   ("Fares and user income", "NA", "-")],
  "C3", ""),
 ("AAM-CAP-01", "Integrated Demand Accommodation Rate", "Confirmed UAM Operational Intents", [
   ("Confirmed UAM Operational Intents", "NS", "UAM §4.3.4, p. 14 (items 3-4)"),
   ("Customer trip requests (denominator)", "IH", "UAM §4.3.2, p. 13; §6.1.1, p. 25"),
   ("Vertiport resource availability", "NS", "UAM §4.3.7, p. 15"),
   ("Corridor availability", "NS", "UAM §4.3.1, p. 12; §4.4, p. 17"),
   ("Fleet and charging availability", "NA", "- (not addressed)")],
  "C2", "Requests the operator cannot serve never become intents; two of the denial causes are invisible to PSUs."),
 ("AAM-CE-01", "Cost per Completed AAM Operation", "Attributable system cost", [
   ("System cost", "NA", "-"),
   ("Completed operations (mission-complete indication, archive)", "PA", "UAM §4.3.4, p. 14 (item 8); §6.1.3, p. 26")],
  "C3", ""),
 ("AAM-EFF-01", "Door-to-Door Travel-Time Benefit", "Door-to-door journey time", [
   ("Ground access and egress times", "NA", "-"),
   ("Flight times (archived operational data)", "PA", "UAM §4.3.4, p. 14 (item 8)"),
   ("Reference-mode journey time", "NA", "-")],
  "C3", ""),
 ("AAM-EFF-02", "Mean AAM Operational Delay", "Actual minus scheduled event times", [
   ("Key event times (departure, arrival) in the confirmed intent", "NS", "UAM §3.2, p. 8; §4.3.2, p. 13"),
   ("Actual departure (automated departure acquisition) and arrival", "PA", "UAM §6.2.2.1, p. 27; §6.1.2, p. 25; §4.3.4, p. 14 (item 8)")],
  "C1", ""),
 ("AAM-ENV-01", "Life-Cycle GHG Intensity", "Life-cycle emissions per unit of output", [
   ("Energy and life-cycle emission data", "NA", "-")],
  "C3", ""),
 ("AAM-ENV-02", "Community Noise Exposure", "Noise exposure of the population", [
   ("Noise levels or acoustic model", "NA", "UAM §4.4, p. 17 (noise as a corridor design consideration only)"),
   ("Flight tracks", "PA", "UAM §6.1.2, p. 25; §4.3.4, p. 14 (item 8)"),
   ("Population data", "NA", "-")],
  "C3", ""),
 ("AAM-FLEX-01", "Successful Operational Replanning Rate", "Successful intent updates", [
   ("Updates to the UAM Operational Intent shared via the network", "NS", "UAM §4.4.2, p. 19"),
   ("Operation outcome (mission complete)", "PA", "UAM §6.1.3, p. 26")],
  "C1", ""),
 ("AAM-FLEX-02", "Degraded-Operation Continuity Rate", "Operations completed under degraded conditions", [
   ("Corridor availability and vertiport open/closed status", "NS", "UAM §4.3.1, p. 12; §4.3.7, p. 15"),
   ("Off-nominal notifications", "NS", "UAM §4.4.2, p. 19"),
   ("Operation outcome (mission complete)", "PA", "UAM §6.1.3, p. 26")],
  "C1", ""),
 ("AAM-GI-01", "Successful Operational Interoperability Rate", "Successful PSU-PSU, PSU-USS and FAA exchanges", [
   ("Exchange attempts and results", "IH", "UAM §2, p. 6; §5, p. 23 (common standards required, not logged)")],
  "C3", ""),
 ("AAM-PART-01", "Effective Stakeholder Engagement Coverage", "Engaged relevant and affected stakeholders", [
   ("Engagement records", "NA", "UAM §1.2.3, p. 2; §4.2, p. 11; §4.3.10, p. 16 (process described, no data)")],
  "C3", ""),
 ("AAM-PRED-01", "Operational Punctuality", "Arrivals within tolerance", [
   ("Scheduled arrival in the confirmed intent", "NS", "UAM §3.2, p. 8"),
   ("Actual arrival (archived operational data)", "PA", "UAM §6.1.2, p. 25; §4.3.4, p. 14 (item 8)")],
  "C1", "The ConOps names a compliance window for the arrival time but does not size it."),
 ("AAM-SAF-01", "Safety Occurrence Rate by Severity", "Safety occurrences", [
   ("Off-nominal event notifications", "NS", "UAM §4.4.2, p. 19; §4.3.1, p. 12"),
   ("Exposure (completed operations)", "PA", "UAM §4.3.4, p. 14 (item 8)"),
   ("Severity classification", "NA", "-")],
  "C2", ""),
 ("AAM-SAF-02", "Ground Third-Party Risk", "Ground risk exposure", [
   ("Population and ground exposure data, risk model", "NA", "-"),
   ("Flight tracks", "PA", "UAM §6.1.2, p. 25")],
  "C3", ""),
 ("AAM-SEC-01", "Cybersecurity Compromise Rate", "Cybersecurity compromises", [
   ("Record of cyber incidents", "NA", "UAM §5, p. 23 (Service Security Gateway named, no record)")],
  "C3", ""),
 ("AAM-SEC-02", "Privacy Incident Rate", "Privacy incidents", [
   ("Record of privacy incidents", "NA", "- (privacy not addressed in the UAM ConOps)")],
  "C3", ""),
]
