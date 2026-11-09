// KPI_Common.sysml
// Shared core: ICAO KPAs, classification metadata, system boundaries and common calculation patterns.
// Generated from article 1 and the E1 source classification. Formulas marked PROPOSED are for article 2.

package KPI_Taxonomy {
    doc /* Enumerations and metadata used to classify KPAs, performance objectives and KPI candidates (article 1: applicability, analytical status, measurement maturity, taxonomic fit). */
    private import ScalarValues::*;

    enum def Domain { enum UTM; enum AAM; }
    enum def Applicability { enum Applicable; enum ConditionallyApplicable; enum NotApplicable; }
    enum def RetentionStatus { enum ProvisionallyRetained; enum ConditionallyRetained; }
    enum def Operationalization {
        doc /* Measurement maturity of the candidate, kept distinct from retention status (article 1). */
        enum ConceptualFormulaInArticle1;
        enum ProposedInThisStudy;
        enum Pending;
    }
    enum def TaxonomicFit { enum Direct; enum Provisional; enum Gap; }

    metadata def KPAApplicability {
        attribute domain : Domain;
        attribute applicability : Applicability;
    }
    metadata def CandidateKPI {
        attribute code : String;
        attribute domain : Domain;
        attribute measurementConstruct : String;
        attribute status : RetentionStatus;
        attribute maturity : Operationalization;
    }
    metadata def DomainExtension {
        doc /* Construct that extends the reference KPA taxonomy for the domain. */
        attribute fit : TaxonomicFit;
    }
    metadata def SupportingDiagnosticMetric {
        doc /* Explains why a system-level KPI behaves as observed; not itself a system-level KPI. */
    }

    enum def SourceClass {
        doc /* Where a KPI input exists according to the FAA concepts of operations (experiment E1).
         * NetworkShared: exchanged across the USS Network or the federated service network during operations.
         * ProviderArchived: retained by USSs, PSUs or operators and available on authorized request.
         * InternallyHeld: exists within one operator or provider, with no sharing or archiving requirement.
         * NotAddressed: no corresponding data element in the concept of operations. */
        enum NetworkShared;
        enum ProviderArchived;
        enum InternallyHeld;
        enum NotAddressed;
    }
    enum def InputRole {
        doc /* Principal: the quantity the KPI counts or measures; Supporting: any other input. */
        enum Principal;
        enum Supporting;
    }
    attribute def KPIInput {
        doc /* A quantity consumed by a KPI candidate, described in its doc and classified by @DataSource. */
    }
    metadata def DataSource {
        doc /* Source class of a data element in the FAA concepts of operations, with the section and printed page. */
        attribute sourceClass : SourceClass;
        attribute conopsRef : String;
    }
    metadata def KPIInputRole {
        doc /* Role of an input in a KPI; on a KPIInput attribute, or on a dependency from a KPI to a data-item attribute. */
        attribute role : InputRole;
    }
}

package ICAO_KPAs {
    doc /* The eleven ICAO ATM reference KPAs (ICAO Doc 9854 and Doc 9883), used as the common performance reference structure. Performance Intents: article 1, Table 1. */

    concern def AccessAndEquity { doc /* ICAO reference KPA: Access and Equity. */ }
    concern def Capacity { doc /* ICAO reference KPA: Capacity. */ }
    concern def CostEffectiveness { doc /* ICAO reference KPA: Cost Effectiveness. */ }
    concern def Efficiency { doc /* ICAO reference KPA: Efficiency. */ }
    concern def Environment { doc /* ICAO reference KPA: Environment. */ }
    concern def Flexibility { doc /* ICAO reference KPA: Flexibility. */ }
    concern def GlobalInteroperability { doc /* ICAO reference KPA: Global Interoperability. */ }
    concern def Participation { doc /* ICAO reference KPA: ATM Community Participation. */ }
    concern def Predictability { doc /* ICAO reference KPA: Predictability. */ }
    concern def Safety { doc /* ICAO reference KPA: Safety. */ }
    concern def Security { doc /* ICAO reference KPA: Security. */ }
}

package System_Boundaries {
    doc /* Selected system boundaries (article 1, Sec. 2.4). */

    part def UTMSystem {
        doc /* Based on the FAA UTM ConOps v2.0: traffic-management services, operational coordination,
         * information exchange, service interactions and constraint management that support
         * unmanned operations. Intrinsic aircraft or propulsion characteristics are excluded. */
    }
    part def AAMSystem {
        doc /* Based on the FAA UAM ConOps v2.0 and AAM Implementation Plan: an integrated mobility
         * system of systems with aircraft operations, traffic-management interactions, vertiports,
         * supporting infrastructure, energy, digital services, ground access, users and affected
         * communities. UAM is treated as the urban subset of AAM. */
    }
}

package KPI_Patterns {
    doc /* Common calculation patterns shared by UTM and AAM candidates. PROPOSED for article 2; not defined in article 1. */
    private import ScalarValues::*;

    abstract calc def AccommodationRate {
        doc /* Accommodated demand over valid demand in a period and volume, in percent. */
        in accommodated : Natural;
        in validDemand : Natural;
        return rate : Real = accommodated / validDemand * 100;
    }
    abstract calc def TemporalConformanceRate {
        doc /* Completed operations whose actual time deviates from the planned time by no more
         * than the tolerance, over all completed operations, in percent. */
        in withinTolerance : Natural;
        in completed : Natural;
        in toleranceSeconds : Real;
        return rate : Real = withinTolerance / completed * 100;
    }
}
