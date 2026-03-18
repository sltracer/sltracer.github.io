import random
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

#本期SP式神，单独列出来。SSR的话另起一个代码。
theme_sp = "本期新SP式神"

# 剩余共47个SP式神
sp_list = [
    "少羽大天狗", "炼狱茨木童子", "稻荷神御馔津", "苍风一目连", "赤影妖刀姬", "御怨般若",
    "骁浪荒川之主", "烬天玉藻前", "鬼王酒吞童子", "天剑韧心鬼切", "聆海金鱼姬", "浮世青行灯",
    "缚骨清姬", "待宵姑获鸟", "麓铭大岳丸", "初翎山风", "夜溟彼岸花", "蝉冰雪女",
    "空相面灵气", "绘世花鸟卷", "因幡辉夜姬", "梦寻山兔", "神堕八岐大蛇", "大夜摩天阎魔",
    "心狩鬼女红叶", "神启荒", "禅心云外镜", "流光追月神", "修罗鬼童丸", "寻森小鹿男",
    "纺愿缘结神", "渺念萤草", "本真三尾狐", "鲸汐千姬", "福悦座敷童子", "晨晖惠比寿",
    "龙吟铃鹿御前", "遥念烟烟罗", "心友犬神", "神酿星熊童子", "瑶音紧那罗", "晴思日和坊",
    "时曜泷夜叉姬", "云间不见岳", "妙主九命猫", "梦引蝴蝶精", "梦山白藏主"
]

# 排除"两面佛"，以及联动式神，均无法从卡池中获取。
# 共56个SSR式神
ssr_list = [
    "大天狗", "酒吞童子", "荒川之主", "阎魔", "小鹿男", "茨木童子",
    "青行灯", "妖刀姬", "一目连", "花鸟卷", "辉夜姬", "荒", "彼岸花", "雪童子",
    "山风", "玉藻前", "御馔津", "面灵气", "鬼切", "白藏主", "八岐大蛇",
    "不知火", "大岳丸", "泷夜叉姬", "云外镜", "鬼童丸", "缘结神", "铃鹿御前",
    "紧那罗", "千姬", "帝释天", "阿修罗", "食灵", "饭笥", "铃彦姬", "不见岳",
    "须佐之男", "寻香行", "季", "月读", "言灵", "孔雀明王", "天照", "伊邪那美",
    "泷", "猫川", "祸津神", "龙珏", "封阳君", "鬼金羊", "歌留多", "卑弥呼",
    "荒骷髅", "雪御前", "平将门", "神无月"
]

# 唯一一个UR式神，由于UR式神不计入小保底，不影响大保底，本质上和SR与R式神没有区别。
ur_list = ["妖刀姬·绯夜猎刃"]

# 不太准确，但是SR名单不是很重要捏。
sr_list = [
    "桃花妖", "雪女", "鬼使白", "鬼使黑", "孟婆", "犬神",
    "骨女", "鬼女红叶", "跳跳哥哥", "傀儡师", "海坊主", "判官",
    "凤凰火", "吸血姬", "妖狐", "妖琴师", "食梦貘", "清姬",
    "镰鼬", "姑获鸟", "二口女", "白狼", "樱花妖", "惠比寿",
    "络新妇", "般若", "青坊主", "夜叉", "黑童子", "白童子",
    "烟烟罗", "金鱼姬", "鸩", "以津真天", "匣中少女", "书翁",
    "百目鬼", "追月神", "薰", "弈", "猫掌柜", "化鲸"
]

# 同上，R名单并不是很重要捏。
r_list = [
    "三尾狐", "座敷童子", "鲤鱼精", "九命猫", "狸猫", "河童",
    "童男", "童女", "饿鬼", "巫蛊师", "鸦天狗", "食发鬼",
    "武士之灵", "雨女", "跳跳弟弟", "跳跳妹妹", "兵俑", "丑时之女",
    "独眼小僧", "铁鼠", "椒图", "管狐", "山兔", "萤草",
    "蝴蝶精", "山童", "首无", "觉", "青蛙瓷器", "古笼火",
    "小袖之手", "虫师", "垢尝", "影鳄"
]

# 合并为完整的104个SSR/SP池（包含当期UP）
all_ssr_sp_pool = ssr_list + sp_list + [theme_sp]   # 56 + 47 + 1 = 104

# 概率参数 继承自task4
P_BASE = 0.0125  # SSR/SP基础概率
P_SP = 0.0025    # SP基础概率
P_SSR = 0.01     # SSR基础概率
P_UR = 0.001      # UR概率
P_SR = 0.20      # SR概率
P_R = 0.7865     # R概率

max_b = 449  # 大保底水位上限
max_s = 59  # 小保底水位上限
p_gift_up = 1.0 / 104     # 赠送式神为当期UP的概率 (根据您的统计103+1)


# 在全局区域定义统计字典（放在主模拟函数外）
gift_stats = {
    "total_gift": 0,      # 触发赠送的总次数
    "up_gift": 0          # 赠送得到UP的次数
}

# 非全集赏SP概率UP活动成长曲线，780为最后一次成长节点，第800抽必出当期SP。
def U(b, allcollect = True):
    if allcollect: 
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
    else:
        if b < 60:
            return 0.03
        elif b < 120:
            return 0.05
        elif b < 180:
            return 0.08
        elif b < 240:
            return 0.10
        elif b < 300:
            return 0.15
        elif b < 360:
            return 0.20
        elif b < 420:
            return 0.25
        elif b < 480:
            return 0.30
        elif b < 540:
            return 0.40
        elif b < 600:
            return 0.50
        elif b < 660:
            return 0.70       
        elif b < 720:
            return 0.80    
        elif b < 780:
            return 0.90             
        else:
            return 1.00


# b:大保底水位，s:小保底水位。
# 先判断是否到达大保底，然后判断是否出货，出货了就判断歪了没，歪了就判断SP还是SSR。没出货就判断是UR、SR、R。
# 然后根据情况更新保底水位。
def simulate_single_pull(b, s, allcollect = True, counter_yjh = 0):
    """单次抽卡模拟"""
    # 确定出货概率
    p_ssr_sp = 1.0 if s == 59 else P_BASE
    
    # 先判断是否抽到SSR/SP
    # 非全集赏大保底检测改为800
    rand = random.random()

    threshold = 0
    if allcollect:
        threshold = 449
    else:
        threshold = 799
        
    if b==threshold:

        return "SP", theme_sp, 0, 0, counter_yjh+1
    
    if rand < p_ssr_sp:
        # SSR/SP出货，这里的random.random是重新生成的一个。
        if random.random() < U(b, allcollect):
            # 抽中UP式神
            return "SP", theme_sp, 0, 0, counter_yjh+1
        else:
            # 歪了，按比例选择SSR或SP，这里的random.random是重新生成的一个。
            if random.random() < 0.2:  # 20%概率歪到其他SP
                chosen = random.choice(sp_list)
                return "SP", chosen, b+1, 0, counter_yjh+1
            else:  # 80%概率歪到其他SSR
                chosen = random.choice(ssr_list)
                new_counter = counter_yjh if s == 59 else 0
                return "SSR", chosen, b+1, 0, new_counter
    elif rand < P_BASE + P_UR:
        return "UR", "妖刀姬·绯夜猎刃", b+1, s+1, counter_yjh+1
    elif rand < P_BASE + P_UR + P_SR:
        return "SR", "随机SR式神", b+1, s+1, counter_yjh+1
    else:
        return "R", "随机R式神", b+1, s+1, counter_yjh+1
        
# 然后这里重复单抽直到抽到当期UP式神，这个代码专门考虑当期式神为SP，考虑SP/SSR式神。
def simulate_until_up(b_start=0, s_start=0, allcollect = True, include_gift = True):
    """
    模拟从初始状态开始，直到抽到当期UP式神
    返回：抽卡次数
    """
    b, s = b_start, s_start
    # pulls 记录抽了多少抽
    pulls = 0
    max_yjh_counter = 0
    current_yjh = 0
    # 总之就是抽到return为止，不然一直循环
    while True:
        pulls += 1
        rarity, name, new_b, new_s, current_yjh = simulate_single_pull(b, s, allcollect, current_yjh)

        max_yjh_counter = max([current_yjh,max_yjh_counter])
        # 如果抽到当期UP式神，结束模拟
        if name == theme_sp:
            if include_gift and pulls == 40:
                gift_stats["total_gift"] += 1          # 赠送次数+1
                random_character = random.choice(all_ssr_sp_pool)
                if random_character == theme_sp:
                    gift_stats["up_gift"] += 1
            return pulls, max_yjh_counter
        
        # 更新保底状态
        b, s = new_b, new_s

        # 40抽赠送
        if include_gift and pulls == 40:
            gift_stats["total_gift"] += 1          # 赠送次数+1
            random_character = random.choice(all_ssr_sp_pool)
            if random_character == theme_sp:
                gift_stats["up_gift"] += 1
                return pulls, max_yjh_counter

# 多跑几次
def run_mass_simulation(num_simulations=10000, b_start=0, s_start=0, allcollect = True):
    """
    运行大规模模拟
    返回：每次模拟所需的抽数列表
    """

    # 建一个list放结果
    results_pulls = []      # 存放抽数
    results_max_yjh = []    # 存放每次模拟的最高月见黑计数
    
    print(f"开始大规模模拟，总次数: {num_simulations}")
    
    # 等号装作分割线
    print("=" * 50)
    
    for i in range(num_simulations):
        pulls_needed, max_yjh_counter = simulate_until_up(b_start, s_start, allcollect)
        results_pulls.append(pulls_needed)
        results_max_yjh.append(max_yjh_counter)
        
        # 显示进度
        step = max(num_simulations // 10, 1)   # 至少为1，避免除零
        if (i + 1) % step == 0:
            progress = (i + 1) / num_simulations * 100
            print(f"进度: {progress:.0f}% ({i + 1}/{num_simulations})")
    
    return results_pulls,results_max_yjh

# 总之分析一下结果
def analyze_results(results,results_yjh, allcollect = True):
    """分析模拟结果 - 简化版"""
    
    # 转一下格式
    results_array = np.array(results)
    
    # 基本统计信息：平均数，中位数，标准差，最低值，最高值。
    mean_pulls = np.mean(results_array)
    median_pulls = np.median(results_array)
    std_pulls = np.std(results_array)
    min_pulls = np.min(results_array)
    max_pulls = np.max(results_array)
    
    # 理论期望值，根据task4结果，考虑40抽赠送SP/SSR，非全集赏抽SP池期望抽数为322.21，全集赏为223.72。
    theoretical_expectation_allcollect = 223.72
    theoretical_expectation_noallcollect = 322.21
    theoretical_expectation = 0
    if(allcollect):
        theoretical_expectation = theoretical_expectation_allcollect
    else:
        theoretical_expectation = theoretical_expectation_noallcollect
    # 印出来看看
    print(f"模拟结果分析（{len(results)}次模拟）")
    print("=" * 50)
    print(f"平均抽数: {mean_pulls:.2f}")
    print(f"中位数: {median_pulls:.2f}")
    print(f"标准差: {std_pulls:.2f}")
    print(f"最小值: {min_pulls}")
    print(f"最大值: {max_pulls}")
    print(f"理论期望值: {theoretical_expectation:.2f}")
    print(f"与理论值误差: {abs(mean_pulls - theoretical_expectation)/theoretical_expectation*100:.2f}%")
    print(f"总共触发赠送次数：{gift_stats['total_gift']}")
    print(f"赠送直接获得UP的次数：{gift_stats['up_gift']}")
    if gift_stats['total_gift'] > 0:
        print(f"赠送获得UP的比例：{gift_stats['up_gift']/gift_stats['total_gift']:.2%}")
    else:
        print("赠送未触发")

    # ---------- 月见黑最高计数分布统计 ----------
    print("\n--- 月见黑最高计数分布 ---")
    bins = [0, 100, 200, 300, 400, 500, float('inf')]
    labels = ['000-099', '100-199', '200-299', '300-399', '400-499', '500-800']
    counts = [0] * (len(bins)-1)
    for value in results_yjh:
        for i in range(len(bins)-1):
            if bins[i] <= value < bins[i+1]:
                counts[i] += 1
                break
    total_yjh = len(results_yjh)
    max_count = max(counts)
    width = len(str(max_count))  # 计算最大计数的位数
    for label, count in zip(labels, counts):
        pct = count / total_yjh * 100
        print(f"{label}: {count:0{width}d} ({pct})")
    
    # 可选：月见黑统计信息
    yjh_array = np.array(results_yjh)
    print(f"\n月见黑最高计数均值: {np.mean(yjh_array):.1f}")
    print(f"月见黑最高计数中位数: {np.median(yjh_array):.1f}")
    return {
        'mean': mean_pulls,
        'median': median_pulls,
        'std': std_pulls,
        'min': min_pulls,
        'max': max_pulls,
        'theoretical': theoretical_expectation
    }

# 画图，总之问问AI
def plot_results(results, stats_dict, allcollect = True):
    """绘制结果可视化图表 - 只保留直方图和箱线图"""

    # 两张图，左右结构展示
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 1. 直方图
    ax1.hist(results, bins=50, alpha=0.7, color='skyblue', edgecolor='black')

    # 两条线分别是理论期望和模拟的平均值 
    ax1.axvline(stats_dict['mean'], color='red', linestyle='dashed', linewidth=2, 
                label=f'模拟平均值: {stats_dict["mean"]:.1f}')
    ax1.axvline(stats_dict['theoretical'], color='green', linestyle='dashed', linewidth=2, 
                label=f'理论期望: {stats_dict["theoretical"]:.1f}')
    
    # 标题、横坐标、纵坐标标注
    ax1.set_xlabel('消耗抽数')
    ax1.set_ylabel('频次')
    ax1.set_title('抽数分布直方图')

    # 标签
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 找出频次最高的6个抽数
    from collections import Counter
    top_6 = Counter(results).most_common(6)
    top_6_values = [val for val, _ in top_6]
    if allcollect:
        ax1.set_xticks([0, 60, 120, 180, 240, 300, 360, 420, 450])
        ax2.set_xticks([0, 60, 120, 180, 240, 300, 360, 420, 450])
    else:
        ax1.set_xticks([0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660,720,800])
        ax2.set_xticks([0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660,720,800])  
    # 设置这些抽数为刻度
    # ax1.set_xticks(top_6_values)
    # ax2.set_xticks(top_6_values)

    # 2. 箱线图（boxplot不错，保留一下，别的多余的删了。
    ax2.boxplot(results, vert=False)
    ax2.set_xlabel('消耗抽数')
    ax2.set_title('抽数分布箱线图')
    ax2.grid(True, alpha=0.3)

    # 计算并标注关键值
    stats = np.percentile(results, [0, 25, 50, 75, 100])
    for i, stat in enumerate(stats):
        ax2.text(stat, 1.1, f'{stat:.0f}', 
                ha='center', fontsize=8)
        
    # 平均值垂线 + 图例
    ax2.axvline(stats_dict['mean'], color='red', linestyle='dashed', linewidth=2,
                label=f'平均值: {stats_dict["mean"]:.1f}')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('gacha_simulation_results.png', dpi=300, bbox_inches='tight')
    plt.show()

# 追加统计一下抽完之后月见黑进度
def plot_yjh_distribution(results_max_yjh):
    """
    绘制月见黑最高计数的饼图分布
    区间：<100, 100-199, 200-299, 300-399, 400-499, 500+
    图例在右上角，格式为：区间: 计数 (占比)
    """
    bins = [0, 100, 200, 300, 400, 500, float('inf')]
    labels = ['000-099', '100-199', '200-299', '300-399', '400-499', '500-800']
    
    # 统计各区间计数
    counts = [0] * (len(bins) - 1)
    for value in results_max_yjh:
        for i in range(len(bins)-1):
            if bins[i] <= value < bins[i+1]:
                counts[i] += 1
                break
    
    total = sum(counts)
    max_count = max(counts)
    width = len(str(max_count))
    # 构造图例标签：区间: 计数 (百分比)
    legend_labels = []
    for label, count in zip(labels, counts):

        pct = f"{count/total*100:.1f}%"
        # 这里为了对其有一些额外的构造
        legend_labels.append(f"{label}: {count:0{width}d} ({pct})")
    
    # 绘制饼图，不显示数值标签
    plt.figure(figsize=(6, 6))
    wedges, texts = plt.pie(counts, labels=None, startangle=90, radius=0.8)
    plt.title('月见黑最高计数分布')
    plt.axis('equal')
    
    # 添加图例，放置于右上角外侧，调整字体大小以保持清晰
    plt.legend(wedges, legend_labels, title="区间: 计数 (占比)", 
               loc='upper right', bbox_to_anchor=(1.3, 1), fontsize=9)
    plt.tight_layout()
    plt.show()


def main(allcollect = True):
    global gift_stats
    gift_stats = {"total_gift": 0, "up_gift": 0}   # 重置赠送统计（必须！）
    """主函数：执行蒙特卡洛模拟 - 简化版"""

    # 设置随机种子，暂时不需要
    random.seed()
    
    # 模拟次数
    num_simulations = 10**5
    width = num_simulations/10
    
    # 运行模拟
    results_pulls, results_max_yjh = run_mass_simulation(num_simulations,0,0, allcollect)

    # 统计每个抽数出现的频次
    max_pull = 800 if not allcollect else 450  # 根据玩家类型设置最大抽数
    freq = [0] * (max_pull + 1)                # 索引对应抽数，0号元素不使用
    for pulls in results_pulls:
        freq[pulls] += 1

    # 将频次保存到文件
    with open('pulls_freq.txt', 'w', encoding='utf-8') as f:
        f.write("# 抽数 频次\n")
        for pulls in range(1, max_pull + 1):
            if freq[pulls] > 0:                # 只输出出现过的抽数（可选）
                f.write(f"{pulls}\t{freq[pulls]}\n")
    print("频次数据已保存到 pulls_freq.txt")
    
    # 分析结果
    stats = analyze_results(results_pulls, results_max_yjh, allcollect)
    
    # 绘制图表
    plot_results(results_pulls, stats, allcollect)
    plot_yjh_distribution(results_max_yjh)
    # 保存结果到文件
    with open('simulation_results.txt', 'w', encoding='utf-8') as f:
        f.write(f"模拟次数: {num_simulations}\n")
        f.write(f"平均抽数: {stats['mean']:.2f}\n")
        f.write(f"中位数: {stats['median']:.2f}\n")
        f.write(f"标准差: {stats['std']:.2f}\n")
        f.write(f"最小值: {stats['min']}\n")
        f.write(f"最大值: {stats['max']}\n")
        f.write(f"理论期望值: {stats['theoretical']:.2f}\n")
        f.write(f"与理论值误差: {abs(stats['mean'] - stats['theoretical'])/stats['theoretical']*100:.2f}%\n")
        f.write("\n=== 赠送机制统计 ===\n")
        f.write(f"总共触发赠送次数: {gift_stats['total_gift']}\n")
        f.write(f"赠送直接获得UP的次数: {gift_stats['up_gift']}\n")
        if gift_stats['total_gift'] > 0:
            f.write(f"赠送获得UP的比例：{gift_stats['up_gift']/gift_stats['total_gift']:.2%}\n")
        else:
            f.write("赠送未触发\n")

        # 添加月见黑区间分布
        f.write("\n=== 月见黑最高计数分布 ===\n")
        bins = [0, 100, 200, 300, 400, 500, float('inf')]
        labels = ['000-099', '100-199', '200-299', '300-399', '400-499', '500-800']
        counts = [0] * (len(bins)-1)
        for value in results_max_yjh:
            for i in range(len(bins)-1):
                if bins[i] <= value < bins[i+1]:
                    counts[i] += 1
                    break
        total = len(results_max_yjh)
        max_count = max(counts) if counts else 0
        width = len(str(max_count))
        for label, count in zip(labels, counts):
            pct = count / total * 100
            f.write(f"{label}: {count:0{width}d} ({pct:.1f}%)\n")

    print(f"\n结果已保存到文件:")
    print("  1. simulation_results.txt (文本结果)")
    print("  2. gacha_simulation_results.png (可视化图表)")


    return results_pulls, results_max_yjh, stats


if __name__ == "__main__":
    main(False)