
# 《阴阳师》PVE伤害公式解析

## 核心伤害公式

### 完整公式

$$
\text{最终伤害} = \left[ (A_B + A_{sl} + A_b - A_d) \times  (CO_{sk} \times DI_{\text{skl}}) \times CritDM \times (\frac{300}{(D_B + D_{sl} + D_b - D_d - DN_t) \times DN_{sk}\times DN_{cl} + 300}) \times (\frac{DD_b \times DT_d}{DD_d \times DT_b} \times DI_{\text{skl}} \times DI_{\text{hi}}) \times FR - S \right] \times DI_{\text{sl}}
$$

$$
\text{最终伤害} = \left[ (最终攻击) \times  (技能乘区) \times （暴击伤害） \times (\frac{300}{最终防御力 + 300}) \times (百分比增伤减伤结果) \times 随机浮动 - 护盾 \right] \times (\text{破势\&心眼加成})
$$

### 关键变量

| 变量 | 含义 |
|------|------|
| **<span style="color: #FF6B6B">最终攻击</span>** | = `A_B + A_sl + A_b - A_d` |
|  ▸ A_B | 基础攻击（面板黑字）|
|  ▸ A_sl | 御魂/觉醒（如大天狗）攻击属性（面板红字）|
|  ▸ A_b | 攻击buff总和|
|  ▸ A_d | 攻击debuff总和|
| **<span style="color: #4ECDC4">技能系数</span>** | = `CO_{sk} × DI_{skl}` |
|  ▸ CO_skl | 技能伤害系数（技能倍率） |
|  ▸ DI_skl | 技能等级加成，阴阳师式神技能等级在提高时不会改变原本技能系数，而是额外添加一个乘区，如lv1-100%,lv2-110%,...,lv5-140%。等级5的技能能比1级技能额外造成40%的伤害。|
| **<span style="color: #45B7D1">CritDM</span>** | 暴击伤害（暴击时生效） |
| **<span style="color: #96CEB4">最终防御</span>** | = `(D_B + D_{sl} + D_b - D_d - DN_t) × DN_{sk} × DN_{cl}` |
|  ▸ D_B | 基础防御（面板黑字）|
|  ▸ D_sl | 御魂/觉醒防御属性（面板红字）|
|  ▸ D_b | 防御buff总和|
|  ▸ D_d | 防御debuff总和|
|  ▸ DN_t | 玉藻前觉醒效果忽略防御100|
|  ▸ DN_sk | 技能无视防御系数（如姑获鸟） |
|  ▸ DN_cl | 网切：50%概率无视45%防御 |
| **<span style="color: #FFEAA7">百分比增减伤结果</span>** | = `(DD_b × DT_d) / (DD_d × DT_b) × DI_sk × DI_hi` |
|  ▸ DD_b | 增伤乘区（1 + 增伤总和） |
|  ▸ DD_d | 造成伤害降低乘区（1 + 降低总和） |
|  ▸ DT_b | 免伤乘区（1 + 免伤总和） |
|  ▸ DT_d | 承伤增加乘区（1 + 承伤增加总和） |
|  ▸ DI_sk | 技能特殊增减伤 |
|  ▸ DI_hi | 鸣屋加成（对处于冰冻、眩晕、睡眠状态单位造成额外45%伤害） |
| **<span style="color: #DDA0DD">FR</span>** | 浮动系数（0.99~1.01） |
| **<span style="color: #98D8C8">S</span>** | 护盾值 |
| **<span style="color: #F7DC6F">DI_sl</span>** | 破势(对生命值高于70%的单位造成额外40%伤害)/心眼（对生命值低于30%的目标额外造成50%伤害） |

