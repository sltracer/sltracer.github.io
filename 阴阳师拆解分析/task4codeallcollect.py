import numpy as np

# 参数设置
p_base = 0.0125  # 基础SSR/SP概率
max_b = 449  # 大保底水位上限
max_s = 59  # 小保底水位上限
p_gift_up = 1.0 / 103     # 赠送式神为当期UP的概率 (根据您的统计: 1/103)

def U(b):
    if b < 60:
        return 0.10
    elif b < 120:
        return 0.12
    elif b < 180:
        return 0.14
    elif b < 240:
        return 0.18
    elif b < 300:
        return 0.25
    elif b < 360:
        return 0.40
    elif b < 420:
        return 0.55
    else:
        return 0.80

# 初始化期望数组
E = np.zeros((max_b + 1, max_s + 1))
for s in range(max_s + 1):
    E[max_b][s] = 1.0  # 边界条件

# 打开文件准备写入详细过程
with open('markov_calculation_details.txt', 'w', encoding='utf-8') as f:
    f.write("《阴阳师》抽卡马尔可夫链模型详细计算过程\n")
    f.write("=" * 60 + "\n")
    f.write(f"模型假设：SSR/SP基础概率 p_base = {p_base}\n")
    f.write(f"大保底触发线：b >= {max_b} 时，下一抽必得UP式神\n")
    f.write(f"小保底触发线：s = {max_s} 时，下一抽必得SSR/SP\n")
    f.write("=" * 60 + "\n\n")
    
    # 按 b 从大到小递推
    for b in range(max_b - 1, -1, -1):
        # 在文件中为每个b值添加一个清晰的分区标题
        f.write(f"\n{'='*40}\n")
        f.write(f"开始计算大保底水位 b = {b:3d} 的所有状态\n")
        f.write(f"{'='*40}\n")
        
        for s in range(max_s + 1):
            # 计算当前状态概率
            P_val = 1.0 if s == max_s else p_base
            up_prob = U(b)
            
            # 状态转移期望计算
            current_step = 1.0
            if s == max_s:
                term_fail = 0.0
            else:
                term_fail = (1 - P_val) * E[b + 1][s + 1]
            term_ssr_nonup = P_val * (1 - up_prob) * E[b + 1][0]
            
            if b==39:
                E[b][s] = p_gift_up*0 + (1-p_gift_up)*(current_step + term_fail + term_ssr_nonup)
            else:
                E[b][s] = current_step + term_fail + term_ssr_nonup                
            # 将当前状态的计算详情写入文件
            f.write(f"状态 (b={b:3d}, s={s:2d}): ")
            f.write(f"P(出货)={P_val:.4f}, U(b)={up_prob:.2f}, ")
            f.write(f"期望 E={E[b][s]:7.3f} 抽")
            # 对于特殊状态，添加备注
            if s == max_s:
                f.write(" [小保底触发]")
            if b >= 420:
                f.write(" [高UP概率区间]")
            f.write("\n")

# 控制台输出关键结果摘要
print("计算完成！详细过程已保存至文件: markov_calculation_details.txt\n")
print("关键结果摘要:")
print(f"全集赏初始状态 (0, 0) 的期望抽数: {E[0][0]:.2f} 抽\n")