<template>
    <el-container>
    <el-header>
        <el-row type="flex" justify="space-between" align="middle">
            <el-col :span="12"><h1 class="page-title">开始翻译</h1></el-col>
            <el-col :span="12" style="text-align: right;">
                <el-button type="primary" plain @click="toEn()" class="action-button">一键机器翻译</el-button>
            </el-col>
        </el-row>
    </el-header>
    <el-main>
        <el-dialog 
          title="编辑内容" 
          fullscreen="true"
          :visible.sync="dialogVisible" 
          width="50%"
          :modal="false">
          <el-form :model="editForm" label-width="100px">
            <el-form-item label="段号">
              <el-input v-model="editForm.id" disabled></el-input>
            </el-form-item>
            <el-form-item label="原文">
              <el-input type="textarea" v-model="editForm.origin" disabled :rows="20"></el-input>
            </el-form-item>
            <el-form-item label="译文">
              <el-input type="textarea" v-model="editForm.target" :rows="20"></el-input>
            </el-form-item>
            <el-form-item label="备注">
              <el-input type="textarea" v-model="editForm.notes"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSave">保存</el-button>
          </span>
        </el-dialog>
        <template>
        <el-table
            :data="tableData"
            border="true"
            style="width: 100%">
            <el-table-column
            fixed
            prop="id"
            label="段号"
            width="50">
            </el-table-column>
            <el-table-column
            prop="direction"
            label="翻译方向"
            width="80">
            </el-table-column>
            <el-table-column
            prop="origin"
            label="原文"
            width="500">
            </el-table-column>
            <el-table-column
            prop="target"
            label="译文"
            width="500">
            </el-table-column>
            <el-table-column
            prop="notes"
            label="备注"
            width="250">
            </el-table-column>
            <el-table-column
            fixed="right"
            label="操作"
            width="200">
            <template slot-scope="scope">
                <el-row>
                    <el-button type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
                </el-row>
                <!-- <el-row>
                    <el-button type="success" icon="el-icon-check" @click="handleSave()">保存</el-button>
                </el-row> -->
                <el-row>
                    <el-button type="success" icon="el-icon-cpu" @click="handleTranslate(scope.row)">机翻</el-button>
                </el-row>        
            </template>
            </el-table-column>
        </el-table>
        </template>
    </el-main>
    </el-container>
</template>

<script>
    import axios from 'axios';
    const md5 = require('js-md5');  //引入md5模块

    export default {
    methods: {
      handleEdit(row) {
        this.editForm = JSON.parse(JSON.stringify(row));
        this.editIndex = this.tableData.findIndex(item => item.id === row.id);
        this.dialogVisible = true;
      },
      handleSave() {
        if(this.editIndex===-1) return;
        else{
          this.$set(this.tableData, this.editIndex, this.editForm);
          this.dialogVisible = false;     
          window.alert("确认保存？")
          // 更新服务器数据
          axios.post(this.url, this.editForm).then(response => {
            this.$message.success(response.data.message);
          })
          .catch(error => {
            this.$message.error('保存失败: ' + error.message);
          });
        }
      },


      handleTranslate(row){
        //window.alert(JSON.stringify(this.tableData[0]))

        const appkey="MmpU7G7RoRp13pX_S_Vs"
        const appid="20250426002343213"
        const salt = Date.now().toString();
        var fromLang,toLang;  

        if(this.tableData.length==0) return;
        if(this.tableData[0].direction==="英译中"){
          fromLang="en";
          toLang="zh";

        }
        else if(this.tableData[0].direction==="中译英"){
          fromLang="zh";
          toLang="en";
        }

        try {
            var item=row
            let query=item.origin; //待翻译文本
            //生成签名sign
            let sign_str = appid + query + salt + appkey
            let sign = md5(sign_str)
            if (item.origin) {
                axios.post('baiduApi', {
                    q: query,
                    from: fromLang,
                    to: toLang,
                    appid: appid,
                    salt: salt,
                    sign: sign
                },{
                    headers:this.headers
                }).then(response => {
                    // 根据百度翻译API的响应格式处理译文
                    // 假设响应格式为：{ "trans_result": [{"dst": "译文内容"}] }
                    if (response.data && response.data.trans_result && response.data.trans_result.length > 0) {
                        item.target = response.data.trans_result.map(result => result.dst).join('\n');
    
                    } else {
                        console.error('翻译失败:', response.data);
                        return;
                    }
                    console.log(query)
                    console.log(response.data.trans_result)
                })
                .catch(error => {
                    console.error('翻译失败:', error);
                    return;
                });
            }
            this.$message.success('翻译完成'); 
        }catch (error) {
            console.error('翻译过程中发生错误:', error);
            this.$message.error('翻译失败');
        }    
      },

      toEn(){
        window.alert("敬请期待...");
      }

    },
    
    data() {
      return {
        tableData: [],
        url: this.HOST+'/translate/',
        dialogVisible: false,
        editForm: {
          id: '',
          direction: '',
          origin: '',
          target: '',
          notes: ''
        },
        editIndex: -1,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    },
    mounted(){
        axios.get(this.url).then(response => {
            this.tableData = response.data.text;
        })
    }
}
</script>

<style>
.el-table .cell {
    word-break: break-word;
    white-space: pre-wrap;
}

.el-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.el-header {
    background: rgba(255,255,255,0.8);
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    padding: 0 30px;
    height: 64px;
}

.page-title {
    color: #2c3e50;
    font-size: 25px;
    font-weight: 600;
    margin: 0;
    line-height: 64px;
    letter-spacing: 1px;
}

.el-main {
    display: flex;
    justify-content: top;
    align-items: top;
    padding: 40px;
    background: transparent;
}

.el-table .el-button {
    width: 80px;
    margin: 2px 0;
    text-align: center; 
}

.action-button {
    padding: 10px 24px;
    font-size: 14px;
    height: 36px;
    margin-top: 14px;
    margin-bottom: 14px;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.action-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
    .action-button {
        padding: 8px 16px;
        font-size: 13px;
    }
}

</style>