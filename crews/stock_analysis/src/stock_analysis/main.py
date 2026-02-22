import sys
from crew import StockAnalysisCrew

def run():
    inputs = {
        'query': '请对该股票进行全面的投资分析',
        'company_stock': '688653',
    }
    return StockAnalysisCrew().crew().kickoff(inputs=inputs)

def train():
    inputs = {
        'query': '分析该股票去年的营收情况',
        'company_stock': '688653',
    }
    try:
        StockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    print("## 欢迎使用A股分析系统")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## 分析报告")
    print("########################\n")
    print(result)
