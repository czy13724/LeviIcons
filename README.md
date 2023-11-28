### Automatic integration of icon json files

#### 简介
作者：[Levi](https://github.com/czy13724)
更新日期：2023.11.27
仓库地址：[LeviIcons](https://github.com/czy13724/LeviIcons)

如果你觉得好用的话，不妨点个✨star，支持一下作者～
#### 功能
基于github aciton自动生成Quantmult X图标订阅。用于将对应仓库所有的图标raw整合为一个json文件，以便Quantumult X，Surge，Loon等软件的图标订阅导入。
 #### 使用方法：
1. 新建一个仓库作为图床，并新建一个文件夹用于存储图片，可随意命名（~~不建议使用中文~~）。   
2. 点击`action`并创建一个工作流（workflow）,将下方代码放入并按照说明进行替换
```shell
name: Generate Image JSON

on:
  push:
    branches:
      - main
    paths:
    # 将下面的LEVI替换为自己的仓库名
      - 'LEVI/*'
  workflow_dispatch:
    inputs:
      dummy-trigger:
        description: 'Dummy trigger for manual run'
        default: 'Run workflow'

  schedule:
    - cron: '0 1 * * *'  # 每天的 UTC+8 09:00 运行

jobs:
  generate-json:
    runs-on: ubuntu-latest

    steps:
    - name: Set up Node.js
      uses: actions/setup-node@v4.0.0
      with:
        node-version: '16'

    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Display Node.js version
      run: node --version

    - name: Debug - Current working directory and list files
      run: |
        pwd
        ls -la
    - name: Generate JSON
      run: |
         # 将下面的levi替换为自己存储图片的文件名
        IMAGES_FOLDER="levi"
        # 将下面的levi.icons.json替换为要生成的图标订阅名称，json格式
        JSON_FILE="levi.icons.json"
        # 将下面的LEVI替换为自己的仓库名
        DESTINATION_FOLDER="LEVI"
        echo "Checking current directory:"
        pwd
        echo "Listing files in leviicons:"
        ls -al $IMAGES_FOLDER
        # Create an empty JSON file
        echo "[]" > $JSON_FILE
        # Create a JSON file header
        echo "{" > $JSON_FILE
        # 双引号里Levi图标订阅可随意修改，用于图标订阅的显示名称
        echo '  "name": "Levi图标订阅",' >> $JSON_FILE
        # 双引号里description内容可随意修改，用于图标订阅描述展示
        echo '  "description": "收集一些自己常用的图标 by @czy13724",' >> $JSON_FILE
        echo '  "icons": [' >> $JSON_FILE
        
        # Populate the array with image information
        for FILE_PATH in $IMAGES_FOLDER/*; do
          if [ -f "$FILE_PATH" ]; then
            FILE_NAME=$(basename "$FILE_PATH")
            # 将czy13724改为自己用户名，LEVI改为仓库名
            RAW_URL="https://raw.githubusercontent.com/czy13724/LEVI/main/$FILE_PATH"
        # If not the first icons, auto-add a comma before the end of the former
          if [ "$FIRST_ITEM" = false ]; then
        # Add a comma before the end of the former
            sed -i '$s/}$/},/' $JSON_FILE
          fi
    
            # Append image information to the JSON file
            echo -n ", " >> $JSON_FILE
            # Add png info to JSON file
            echo '  {' >> $JSON_FILE
            echo '    "name": "'$FILE_NAME'",' >> $JSON_FILE
            echo '    "url": "'$RAW_URL'"' >> $JSON_FILE
            echo '  },' >> $JSON_FILE
          fi
        done

            # remove the last comma
            sed -i '$s/,$//' $JSON_FILE

            # Add the end of the last
            echo ']' >> $JSON_FILE
            echo '}' >> $JSON_FILE
            
        # Remove the leading comma
        sed -i 's/^\(.\{2\}\)//' $JSON_FILE

        echo "Checking generated JSON file:"
        cat $JSON_FILE
      
        # Set an environment variable with the path to the JSON file
        #下方LEVI改为自己仓库名
        echo "ARTIFACT_PATH=LEVI" >> $GITHUB_ENV

    - name: Upload Artifact
      uses: actions/upload-artifact@v2
      with:
      # 将levi.icon.json改为上面的图标订阅名称，json格式
        name: levi.icon.json
        path: ${{ env.ARTIFACT_PATH }}

    - name: Push to LEVI Repository
      run: |
        git config user.name "${{ github.actor }}"
        git config user.email "${{ github.actor }}@users.noreply.github.com"
        git add .
        git commit -m "Add generated JSON file"
        git push origin HEAD:main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
```
3. 手动运行一次检查在日志Generate JSON这一栏里查看是否能历遍出所有的图标raw以及是否会出现其他错误。

#### 注意事项
1. 已知错误有：Upload Artifact这里报错可以通过修改路径或在仓库下新建一个package.json文件解决。修改路径在echo "ARTIFACT_PATH=LeviIcons" >> $GITHUB_ENV这里，修改等号后的LeviIcons即可。

 #### 免责声明
* 项目内所涉及脚本、LOGO 仅为资源共享、学习参考之目的，不保证其合法性、正当性、准确性；切勿使用项目做任何商业用途或牟利；

* 遵循避风港原则，若有图片和内容侵权，请在 Issues 告知，核实后删除，其版权均归原作者及其网站所有；
* 本人不对任何内容承担任何责任，包括但不限于任何内容错误导致的任何损失、损害;
* 其它人通过任何方式登陆本网站或直接、间接使用项目相关资源，均应仔细阅读本声明，一旦使用、转载项目任何相关教程或资源，即被视为您已接受此免责声明。

* 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

* 本项目涉及的数据由使用的个人或组织自行填写，本项目不对数据内容负责，包括但不限于数据的真实性、准确性、合法性。使用本项目所造成的一切后果，与本项目的所有贡献者无关，由使用的个人或组织完全承担。

* 本项目中涉及的第三方硬件、软件等，与本项目没有任何直接或间接的关系。本项目仅对部署和使用过程进行客观描述，不代表支持使用任何第三方硬件、软件。使用任何第三方硬件、软件，所造成的一切后果由使用的个人或组织承担，与本项目无关。

* 本项目中所有内容只供学习和研究使用，不得将本项目中任何内容用于违反国家/地区/组织等的法律法规或相关规定的其他用途。

* 所有基于本项目源代码，进行的任何修改，为其他个人或组织的自发行为，与本项目没有任何直接或间接的关系，所造成的一切后果亦与本项目无关。

* 所有直接或间接使用本项目的个人和组织，应24小时内完成学习和研究，并及时删除本项目中的所有内容。如对本项目的功能有需求，应自行开发相关功能。

* 本项目保留随时对免责声明进行补充或更改的权利，直接或间接使用本项目内容的个人或组织，视为接受本项目的特别声明。
