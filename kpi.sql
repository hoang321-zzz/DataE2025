--CTE to compare revenue and KPI    
WITH DoanhThuKPI AS (
    SELECT 
        FORMAT([Ngày_hạch_toán], 'yyyy-MM') AS YearMonth,        -- Create YearMonth in dulieubanhang
        [Chi_nhánh],
        SUM([Doanh_thu]) AS TongDoanhThu
    FROM [dbo].[dulieubanhang]
    GROUP BY 
        FORMAT([Ngày_hạch_toán], 'yyyy-MM'), 
        [Chi_nhánh]
)
SELECT 
    dt.YearMonth AS Thang,
    cn.[Tên_chi_nhánh],
    dt.TongDoanhThu AS DoanhThuThucTe,
    kpi.KPI AS MucTieuKPI,
    (dt.TongDoanhThu - kpi.KPI) AS ChenhLech,
    ROUND((dt.TongDoanhThu / kpi.KPI) * 100, 2) AS percent_of_kpi     -- % of kpi
FROM DoanhThuKPI dt
JOIN [dbo].[chinhanh] cn 
    ON dt.[Chi_nhánh] = cn.Mã_chi_nhánh
JOIN [KPI] kpi 
    ON dt.YearMonth = kpi.[YearMonth] AND dt.Chi_nhánh = kpi.Mã_chi_nhánh
ORDER BY 
    dt.YearMonth ASC, 
    percent_of_kpi DESC;    