<template>
    <el-container>
    <el-header>
        <h1>请选择你要上传的文件</h1>
    </el-header>
    <el-main>
        <el-upload
        class="upload-demo"
        ref="upload"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="(file, fileList) => this.fileList = fileList"
        :file-list="fileList"
        :auto-upload="false"
        :show-file-list="true">
        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">只能上传txt或pdf文件，且不超过500kb</div>
        </el-upload>
    </el-main>
    </el-container>
</template>

<style>
.el-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.el-header {
    background: rgba(255,255,255,0.8);
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    display: flex;
    justify-content: left;
    align-items: center;
}

.el-header h1 {
    color: #2c3e50;
    font-size: 24px;
    margin: 0;
}

.el-main {
    display: flex;
    justify-content: center;
    align-items: center;
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

<script>
    import axios from 'axios';
    
    export default {
    data() {
      return {
        fileList: [],
        uploadUrl: this.HOST+'/uploadfile/',
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      };
    },
    methods: {
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
          console.log(response.data);
          //上传成功后跳转
          this.$router.push('/translate');
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
      }
    }
  }
</script>