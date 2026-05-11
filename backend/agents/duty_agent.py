from config import settings

class DutyAgent:
    def calculate_duty(self, cif_usd: float, hs_data: dict, is_filer: bool = True) -> dict:
        """
        Calculates Pakistan import duties.
        cif_usd: CIF value in USD
        hs_data: dictionary containing cd_rate, rd_rate, acd_rate, st_rate, wht_filer, wht_nonfiler
        """
        pkr_rate = settings.pkr_exchange_rate
        cif_pkr = cif_usd * pkr_rate
        
        cd_rate = hs_data.get('cd_rate', 0) / 100
        rd_rate = hs_data.get('rd_rate', 0) / 100
        acd_rate = hs_data.get('acd_rate', 0) / 100
        st_rate = hs_data.get('st_rate', 0) / 100
        
        wht_key = 'wht_filer' if is_filer else 'wht_nonfiler'
        wht_rate = hs_data.get(wht_key, 0) / 100

        cd_amount = cif_pkr * cd_rate
        rd_amount = cif_pkr * rd_rate
        acd_amount = cif_pkr * acd_rate 
        
        value_for_st = cif_pkr + cd_amount + rd_amount + acd_amount
        st_amount = value_for_st * st_rate
        
        value_for_wht = value_for_st + st_amount
        wht_amount = value_for_wht * wht_rate
        
        total_taxes = cd_amount + rd_amount + acd_amount + st_amount + wht_amount
        
        markdown_table = f"""### Duty & Tax Breakdown (Estimated)
| Component | Rate | Amount (PKR) |
|---|---|---|
| Assessed Value (CIF) | - | {cif_pkr:,.2f} |
| Customs Duty (CD) | {cd_rate*100:.1f}% | {cd_amount:,.2f} |
| Regulatory Duty (RD) | {rd_rate*100:.1f}% | {rd_amount:,.2f} |
| Additional CD (ACD) | {acd_rate*100:.1f}% | {acd_amount:,.2f} |
| Sales Tax (ST) | {st_rate*100:.1f}% | {st_amount:,.2f} |
| Withholding Tax (WHT) | {wht_rate*100:.1f}% | {wht_amount:,.2f} |
| **Total Duties & Taxes** | - | **{total_taxes:,.2f}** |
"""
        
        raw_data = {
            "CIF Value": cif_pkr,
            "Customs Duty (CD)": cd_amount,
            "Regulatory Duty (RD)": rd_amount,
            "Additional Customs Duty (ACD)": acd_amount,
            "Sales Tax (ST)": st_amount,
            "Withholding Tax (WHT)": wht_amount,
            "Total Taxes": total_taxes,
            "Landed Cost": cif_pkr + total_taxes
        }
        return {"markdown": markdown_table, "raw_data": raw_data}
