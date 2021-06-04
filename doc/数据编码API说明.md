# 数据编码

## 数据来源编码

###### 3位

- 编解码参数的对应关系如下：

  ```py
  source = {
      '公网': '101',
      '通信网': '202',
      '电网': '203',
      '微博': '301',
      '川滇': '401',
      '基本震情': '501'
  }
  ```

- 编码API：`get_source_code(source_key: source_str) -> str`

  - 根据传入的source_string返回一个长度为三的数字串string

- 解码API：`get_source_desc(code) -> str`

  - 根据传入的3位code字符串返回对应的来源字符串，并加以**描述**

    ```py
    return '数据来源：' + source_value[source_code]
    ```

## 灾情数据编码

###### 19位

- 12位 地理（省（2）+地级市（2）+县级市（2）+000000）
- 7位 灾情（代码（3）+ index（3）+ 破坏等级（1））

- 参数对应关系：

  - location_str
    - 非直辖市：xxx省xxx市xxx县(区)
    - 直辖市：xxx市xxx区

  - disaster_info_key

    ```py
    disaster_info = {
        '人员伤亡及失踪-死亡': '111',
        '人员伤亡及失踪-受伤': '112',
        '人员伤亡及失踪-失踪': '113',
        '房屋破坏-土木': '221',
        '房屋破坏-砖木': '222',
        '房屋破坏-砖混': '223',
        '房屋破坏-框架': '224',
        '房屋破坏-其他': '225',
        '生命线工程灾情-交通': '331',
        '生命线-供水': '332',
        '生命线-输油': '333',
        '生命线-燃气': '334',
        '生命线-电力': '335',
        '生命线-通信': '336',
        '生命线-水利': '337',
        '次生灾害-崩塌': '441',
        '次生灾害-滑坡': '442',
        '次生灾害-泥石流': '443',
        '次生灾害-岩溶塌陷': '444',
        '次生灾害-地裂缝': '445',
        '次生灾害-地面沉降': '446',
        '次生灾害-其他': '447',
        '震情-基本震情': '551',
        '震情-灾情预测': '552'
    }
    ```

  - disaster_grade_str

    ```py
    disaster_grade = {
        '特大': '0',
        '重大': '1',
        '较大': '2',
        '一般': '3'
    }
    ```

- 编码API：`get_disaster_code(location_key: location_str, disaster_info_key: disaster_info_str, index: int, disaster_grade_key: disaster_grade_str)`

- 解码API：`def get_disaster_desc(code, quantity: int)`

  - **描述**：`'第{index}号灾情信息：发生在{location}的[{grade}]地震灾害造成{info}{quantity}起'`

### 基础地理信息编码

- 由于只精确到县级行政区，因此编码后的返回值为6位有效值+6位0

- 编码API：`def get_location_code(location_key)`
- 无解码API

### 灾情信息编码

- 编码API：`get_disaster_info_code(disaster_info_key, index, disaster_grade_key)`
- 无解码API

## 基本震情编码

###### 26位

- 12位地理
- 14位时间（年（4）+ 月（2）+ 日（2）+ 时（2）+ 分）（2）+ 秒（2））

- location_key同上
- time_key的格式：
  - xxxx年xx月xx日xx时xx分xx秒

- 编码API：`def get_base_code(location_key: str, time_key: str)`
- 解码API：`get_base_desc(code: str)`
  - 描述：`{year}年{month}月{day}日{hour}时{minute}分{second}秒{location}发生地震`

