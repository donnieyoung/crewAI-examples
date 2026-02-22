import akshare as ak
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class StockFinancialToolSchema(BaseModel):
    stock_code: str = Field(..., description="A股股票代码，如 688653")


class StockFinancialTool(BaseTool):
    name: str = "A股财务报表查询"
    description: str = "查询A股上市公司的财务报表数据，包括利润表、资产负债表、现金流量表等关键财务指标。"
    args_schema: Type[BaseModel] = StockFinancialToolSchema

    def _run(self, stock_code: str) -> str:
        try:
            results = []

            # 利润表
            df = ak.stock_financial_report_sina(stock=f"sh{stock_code}", symbol="利润表")
            if df is not None and not df.empty:
                results.append("=== 利润表（最近2期）===")
                results.append(df.iloc[:, :3].to_string())

            # 资产负债表
            df2 = ak.stock_financial_report_sina(stock=f"sh{stock_code}", symbol="资产负债表")
            if df2 is not None and not df2.empty:
                results.append("\n=== 资产负债表（最近2期）===")
                results.append(df2.iloc[:, :3].to_string())

            return "\n".join(results) if results else "未找到财务数据"
        except Exception as e:
            return f"获取财务数据失败: {e}"


class StockNewsToolSchema(BaseModel):
    stock_code: str = Field(..., description="A股股票代码，如 688653")


class StockNewsTool(BaseTool):
    name: str = "A股新闻公告查询"
    description: str = "查询A股上市公司的最新新闻、公告和市场动态。"
    args_schema: Type[BaseModel] = StockNewsToolSchema

    def _run(self, stock_code: str) -> str:
        try:
            results = []

            # 东方财富个股新闻
            df = ak.stock_news_em(symbol=stock_code)
            if df is not None and not df.empty:
                results.append("=== 最新新闻（最近10条）===")
                for _, row in df.head(10).iterrows():
                    results.append(f"[{row.get('发布时间', '')}] {row.get('新闻标题', '')}")

            return "\n".join(results) if results else "未找到新闻数据"
        except Exception as e:
            return f"获取新闻数据失败: {e}"


class StockInfoToolSchema(BaseModel):
    stock_code: str = Field(..., description="A股股票代码，如 688653")


class StockInfoTool(BaseTool):
    name: str = "A股基本信息与行情查询"
    description: str = "查询A股上市公司的基本信息、股价行情、市盈率、市值等数据。"
    args_schema: Type[BaseModel] = StockInfoToolSchema

    def _run(self, stock_code: str) -> str:
        try:
            results = []

            # 基本信息
            df = ak.stock_individual_info_em(symbol=stock_code)
            if df is not None and not df.empty:
                results.append("=== 基本信息 ===")
                results.append(df.to_string(index=False))

            # 历史行情（最近30天）
            df2 = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
            if df2 is not None and not df2.empty:
                results.append("\n=== 近30日行情 ===")
                results.append(df2.tail(30).to_string(index=False))

            return "\n".join(results) if results else "未找到行情数据"
        except Exception as e:
            return f"获取行情数据失败: {e}"
