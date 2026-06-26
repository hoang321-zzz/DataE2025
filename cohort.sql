WITH CustomerCohort AS (
    SELECT
        [Mã_KH],
        DATEADD(month, DATEDIFF(month, 0, MIN([Ngày_hạch_toán])), 0) AS CohortMonth
    FROM dbo.dulieubanhang
    WHERE [Số_lượng_bán] > 0
      AND [Doanh_thu] > 0
      AND [Mã_KH] IS NOT NULL
    GROUP BY [Mã_KH]
),
CohortData AS (
    SELECT
        FORMAT(cc.CohortMonth, 'yyyy-MM') AS CohortMonth,
        DATEDIFF(month, cc.CohortMonth,
            DATEADD(month, DATEDIFF(month, 0, bh.[Ngày_hạch_toán]), 0)
        ) AS CohortIndex,
        COUNT(DISTINCT bh.[Mã_KH]) AS Customers
    FROM CustomerCohort cc
    JOIN dbo.dulieubanhang bh ON cc.[Mã_KH] = bh.[Mã_KH]
    WHERE bh.[Số_lượng_bán] > 0
      AND bh.[Doanh_thu] > 0
    GROUP BY
        cc.CohortMonth,
        DATEDIFF(month, cc.CohortMonth,
            DATEADD(month, DATEDIFF(month, 0, bh.[Ngày_hạch_toán]), 0)
        )
)
SELECT
    CohortMonth,
    [0]  AS Month_0,
    [1]  AS Month_1,
    [2]  AS Month_2,
    [3]  AS Month_3,
    [4]  AS Month_4,
    [5]  AS Month_5,
    [6]  AS Month_6,
    [7]  AS Month_7,
    [8]  AS Month_8,
    [9]  AS Month_9,
    [10] AS Month_10,
    [11] AS Month_11
FROM CohortData
PIVOT (
    SUM(Customers)
    FOR CohortIndex IN ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11])
) AS PivotTable
ORDER BY CohortMonth