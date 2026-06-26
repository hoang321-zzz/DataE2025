--CTE to identify if there are duplicate records
WITH DuplicateRecords AS (
	SELECT
		[Ngày_hạch_toán],
		[Đơn_hàng],
		[Mã_KH],
		[Mã_Sản_Phẩm],
		[Số_lượng_bán],
		[Đơn_giá],
		[Doanh_thu],
		[Giá_vốn_hàng_hóa],
		[Mã_nhân_viên_bán],
		[Chi_nhánh],
		ROW_NUMBER() OVER(
			PARTITION BY [Ngày_hạch_toán],[Mã_KH],[Mã_Sản_Phẩm],[Số_lượng_bán],[Đơn_giá],[Doanh_thu],[Giá_vốn_hàng_hóa],[Mã_nhân_viên_bán],[Chi_nhánh]
			ORDER BY [Đơn_hàng]
			) AS row_num
	FROM dbo.dulieubanhang
)

SELECT [Ngày_hạch_toán],
		[Đơn_hàng],
		[Mã_KH],
		[Mã_Sản_Phẩm],
		[Số_lượng_bán],
		[Đơn_giá],
		[Doanh_thu],
		[Giá_vốn_hàng_hóa],
		[Mã_nhân_viên_bán],
		[Chi_nhánh]
FROM DuplicateRecords
WHERE row_num = 1
ORDER BY Đơn_hàng
