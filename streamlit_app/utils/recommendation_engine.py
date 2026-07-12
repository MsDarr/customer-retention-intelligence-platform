
def assign_recommended_action(row):

    if row["BusinessSegment"] == "Protect Immediately":
        return "Immediate personalized retention outreach"

    if row["BusinessSegment"] == "Maintain Relationship":
        return "Maintain loyalty and strengthen engagement"

    if row["BusinessSegment"] == "Retention Opportunity":
        return "Provide cost-effective retention offer"

    return "Continue standard customer management"


def assign_retention_offer(row):

    if (
        row["RiskCategory"] == "Critical"
        and row["Contract"] == "Month-to-month"
    ):
        return "Annual contract discount and loyalty credit"

    if (
        row["SupportUsageScore"] <= 1
        and row["RiskCategory"] in ["High", "Critical"]
    ):
        return "Complimentary technical support package"

    if (
        row["ServiceCount"] <= 2
        and row["RiskCategory"] in ["High", "Critical"]
    ):
        return "Discounted service bundle"

    if row["BusinessSegment"] == "Maintain Relationship":
        return "Loyalty reward or premium benefit"

    if row["RiskCategory"] == "Moderate":
        return "Targeted promotional offer"

    return "No immediate financial incentive required"


def assign_contact_channel(row):

    if row["RetentionPriority"] == "Immediate Action":
        return "Retention specialist phone call"

    if row["RetentionPriority"] == "High Priority":
        return "Personalized email and phone follow-up"

    if row["RetentionPriority"] == "Monitor":
        return "Automated email or in-app message"

    return "Standard marketing communication"


def assign_recommendation_reason(row):

    reasons = []

    if row["RiskCategory"] in ["High", "Critical"]:
        reasons.append("elevated predicted churn risk")

    if row["CustomerValueGroup"] == "High Value":
        reasons.append("high customer value")

    if row["Contract"] == "Month-to-month":
        reasons.append("flexible month-to-month contract")

    if row["ServiceCount"] <= 2:
        reasons.append("low service adoption")

    if row["SupportUsageScore"] <= 1:
        reasons.append("limited support-service usage")

    if not reasons:
        return "stable customer profile"

    return ", ".join(reasons)


def calculate_recommendation_priority_score(row):

    return round(
        (
            row["ChurnProbability"] * 0.60
            +
            (row["CustomerValueScore"] / 100) * 0.40
        )
        * 100,
        2
    )
