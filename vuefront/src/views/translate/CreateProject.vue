<template>
    <el-container>
    <el-header>
        <el-row type="flex" justify="space-between" align="middle">
            <el-col :span="12"><h1 class="page-title">欢迎, {{ this.username }}!</h1></el-col>
            <el-col :span="12" style="text-align: right;">
                <el-button type="primary" plain icon="el-icon-user" class="action-button">导出</el-button>
            </el-col>
        </el-row>     
    </el-header>
    <el-main>
        <el-row
        class="upload-demo">
            <el-row :gutter="20" style="padding-bottom: 20px;"><h3>新建一个项目</h3></el-row>

            <el-row :gutter="20" style="padding-bottom: 20px;">
                <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item label="项目名称">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>

                    <el-form-item label="项目类型">
                        <el-radio-group v-model="form.type">
                        <el-radio label="英译中"></el-radio>
                        <el-radio label="中译英"></el-radio>
                        </el-radio-group>
                    </el-form-item>

                    <el-form-item label="项目简介">
                        <el-input type="textarea" v-model="form.description"></el-input>
                    </el-form-item>
                    
                </el-form>
            </el-row>

            <el-row>
                <el-upload
                ref="upload"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :on-change="(file, fileList) => this.fileList = fileList"
                :file-list="fileList"
                :auto-upload="false"
                :show-file-list="true">
                <el-button slot="trigger" size="small" type="primary">选取文件</el-button>             
                <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传文件</el-button>
                <div slot="tip" class="el-upload__tip">*只能上传txt或pdf文件，且不超过500kb</div> 
                </el-upload>
            </el-row>

            <el-row :gutter="20" style="padding-top: 50px;">
                <el-form ref="form" :model="form" label-width="80px">
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">立即创建</el-button>
                    <el-button>取消</el-button>
                </el-form-item>
                </el-form>
            </el-row>      
        </el-row>

        <el-row
        class="table-demo">
            <el-row style="padding-top: 20px;"><h3>项目列表</h3></el-row>
            <el-table
                :data="tableData"
                border
                style="width: 100%">
                <el-table-column
                prop="id"
                label="项目编号"
                width="80">
                </el-table-column>
                <el-table-column
                prop="type"
                label="项目类型"
                width="80">
                </el-table-column>
                <el-table-column
                prop="name"
                label="项目名称"
                width="420">
                </el-table-column>
                <el-table-column
                prop="description"
                label="项目简介"
                width="410">
                </el-table-column>
                <el-table-column
                label="操作"
                width="80">
                    <template slot-scope="scope">
                        <el-col>
                            <el-button 
                                type="text"
                                style="color: blue;"
                                @click="toTranslate(scope.row.id,scope.row.name)">
                            编辑</el-button>
                        </el-col>
                        <el-col>
                            <el-button 
                                type="text"
                                style="color: crimson;align-items: center;"
                                @click="deleteProject(scope.row.id,scope.row.name)">
                            删除</el-button>
                        </el-col>                 
                    </template>    
                </el-table-column>
            </el-table>
        </el-row>       
    </el-main>
    </el-container>
</template>

<script>
    import axios from 'axios';

    export default {
    methods: {
        onSubmit() {
            if (!this.form.name || !this.form.name.trim()) {
                this.$message.warning('请输入项目名称');
                return;
            }
            
            if (!this.form.type) {
                this.$message.warning('请选择项目类型');
                return;
            }
            if (this.fileList.length === 0 || this.fileUploaded === false) {
                this.$message.warning('请先上传文件哦');
                return;
            }
            this.form.id=(this.projectNum+1); //设置新项目的编号
            

            axios.post(this.HOST+'/createproject/',this.form).then(
                response=>{
                    this.$message.success('项目创建成功');
                    console.log(response);
                }
            ).catch(error=>{
                this.$message.error('项目创建失败');
                console.error(error);
            });

            this.$message.success('项目创建成功');
            console.log('项目创建:', this.form);
            //创建成功后刷新
            window.location.reload();
        },
        
        submitUpload() {
            if (this.fileList.length === 0) {
                this.$message.warning('请先选择文件');
                return;
            }
            
            const formData = new FormData();
            this.fileList.forEach(file => {
            formData.append('file', file.raw);
            });
            
            axios.post(this.uploadUrl, formData, {
            headers: this.headers,
            onUploadProgress: progressEvent => {
                const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
                );
                console.log(percentCompleted);
                this.$message.info(`上传进度: ${percentCompleted}%`);
            }
            })
            .then(response => {
            this.$message.success('上传成功');
            this.fileUploaded = true;
            console.log(response.data);
            })
            .catch(error => {
            this.$message.error('上传失败');
            console.error(error);
            });
      },


      handleRemove(file, fileList) {
        this.fileList = fileList;
      },
      handlePreview(file) {
        console.log(file);
      },
      toTranslate(rowid,rowname){
        this.$store.dispatch('updateSelectedPrjId',rowid);
        this.$store.dispatch('updateSelectedPrjName',rowname);
        sessionStorage.setItem('store',JSON.stringify(this.$store.state))   //保存状态到sessionStorage中

        this.selectedPrjId = rowid;
        this.selectedPrjName = rowname;

        this.$router.push('/translate')
        //this.$router.push({name:'translate',params:{selectedProjectId:this.selectedPrjId,selectedProjectName:this.selectedPrjName}});
      },

      deleteProject(rowid,rowname){
        window.alert("确认删除？")
        this.form.id=rowid;
        this.form.name=rowname;
        this.form.type='delete';

        axios.post(this.HOST+'/createproject/',this.form).then(
                response=>{
                    this.$message.success('项目删除成功');
                    console.log(response);
                }
            ).catch(error=>{
                this.$message.error('项目删除失败');
                console.error(error);
            });

            //删除成功后刷新
            window.location.reload();
      }
    },

    data() {
      return {
        uploadUrl: this.HOST+'/uploadfile/',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        fileList:[],
        tableData:[],
        form: {
          id: 0,
          name: '',
          type:'',
          description: '',
        },
        username: '',
        projectNum:0,
        fileUploaded:false,
        selectedPrjId:0,
        selectedPrjName:''
      }
    },

    /* 获取用户名和用户项目信息 */
    mounted() {
        axios.get(this.HOST+'/createproject/').then(response => {
            this.username = response.data.username || '用户';
            this.tableData = response.data.projectList;
            this.projectNum = response.data.projectList.length;
            this.fileUploaded = false;
        }).catch(error => {
            console.error('获取用户名失败:', error);
            this.username = '用户';
        })
    },
}
</script>

<style>
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

/* @media (max-width: 768px) {
    .el-header {
        padding: 0 15px;
    }
    .page-title {
        font-size: 18px;
    }
    .action-button {
        padding: 8px 16px;
        font-size: 13px;
    }
} */

.el-main {
    display: flex;
    justify-content: top; 
    align-items: top;
    padding: 40px;
    background: transparent;
}

.upload-demo {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    width: 100%;
    max-width: 600px;
}

.table-demo {
    margin-left: 15px;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    width: 100%;
    max-width: 1120px;
}

.el-upload__tip {
    margin-top: 15px;
    font-size: 14px;
    color: #606266;
}

.el-button--primary {
    background: #409EFF;
    border-color: #409EFF;
}

.el-button--success {
    background: #67C23A;
    border-color: #67C23A;
}
</style>