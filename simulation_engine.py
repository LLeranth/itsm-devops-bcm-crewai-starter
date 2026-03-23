class SimulationEngine:
    def evaluate(self, final_plan: str, scenario: str) -> dict:
        """
        Scores the agent's recovery plan against real BCM KPIs.
        Used by instructor for objective grading.
        """
        plan_lower = final_plan.lower()
        
        rto_met = "within 4 hours" in plan_lower or "under 240 minutes" in plan_lower
        rpo_met = "15 minutes" in plan_lower or "rpo" in plan_lower and "15" in plan_lower
        services_restored = 85 if "mobile banking" in plan_lower and "fraud detection" in plan_lower else 60
        comms_quality = 90 if "customer notification" in plan_lower and "executive briefing" in plan_lower else 50
        
        score = {
            "rto_met": rto_met,
            "rpo_met": rpo_met,
            "services_restored_pct": services_restored,
            "customer_impact_score": 100 - (100 - services_restored) * 0.6,
            "total_recovery_cost": 125000 if rto_met else 450000,
            "overall_kpi_score": round((services_restored + comms_quality) / 2, 1),
            "scenario": scenario
        }
        print("\n🔬 SIMULATION ENGINE EVALUATION:")
        for k, v in score.items():
            print(f"   {k}: {v}")
        return score