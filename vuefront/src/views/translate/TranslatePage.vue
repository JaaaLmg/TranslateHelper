<template>
    <el-container>
    <el-header>
        <el-row type="flex" justify="space-between" align="middle">
            <el-col :span="12"><h1 class="page-title">开始翻译:{{ this.$store.getters.getSelectedPrjName }}</h1></el-col>
            <el-col :span="12" style="text-align: right;">
                <el-button type="primary" plain @click="toEn()" class="action-button">返回主页</el-button>
            </el-col>
        </el-row>
    </el-header>
    <el-main>
        <el-dialog  
          title="开始编辑"
          fullscreen="true"
          :visible.sync="dialogVisible" 
          width="50%"
          :modal="false">
          <el-row class="demo-autocomplete">
            <el-col :span="12">
              <el-autocomplete
                class="inline-input"
                style="margin-bottom:20px"
                v-model="state1"
                :fetch-suggestions="querySearch"
                placeholder="在记忆库中搜索"
                @select="handleSelect"
              ></el-autocomplete>
              <el-button 
                icon="el-icon-search" 
                circle 
                style="margin-left:10px;margin-right:20px" 
                @click="searchMemory()"
                :loading="memorySearchLoading">
              </el-button>

              <el-autocomplete
                class="inline-input"
                style="margin-bottom:20px"
                v-model="state2"
                :fetch-suggestions="querySearch"
                placeholder="在术语库中搜索"
                @select="handleSelect"
              ></el-autocomplete>
              <el-button 
                icon="el-icon-search" 
                circle 
                style="margin-left:10px" 
                @click="searchTerm()"
                :loading="termSearchLoading">
              </el-button>
            </el-col>
            
          </el-row>
          <el-row>
            <el-button 
              icon="el-icon-plus" 
              plain
              style="margin-bottom:30px" 
              @click="handleAddMemory">添加翻译对到记忆库
            </el-button>
            
            <el-button 
              icon="el-icon-plus" 
              plain
              style="margin-bottom:30px" 
              @click="handleAddTerm">添加术语到术语库
            </el-button>
          </el-row>
          
          <el-dialog
            title="记忆库检索结果"
            :visible.sync="memorySearchResultVisible"
            :modal="false"
            width="60%"
            top="5vh"
            custom-class="search-result-dialog">
              <el-descriptions 
                v-for="(item,index) in memorySearchResults" 
                :key="index"
                :column="1"
                border
                style="margin-bottom: 50px;"
                size="medium"
                class="result-item">
                <el-descriptions-item label="原文" label-class-name="text-label narrow-first-column">
                  <div class="fixed-text-box">{{ item.origin }}</div>
                </el-descriptions-item>
                <el-descriptions-item label="译文" label-class-name="text-label">
                  <div class="fixed-text-box">{{ item.target }}</div>
                </el-descriptions-item>
              </el-descriptions>

              <h3>查看和修改</h3>
              <el-table
              :data="this.memorySearchResults"
              style="width: 100%">
              <el-table-column
                label="原文"
                width="180">
                <template slot-scope="scope">
                  <span style="margin-left: 10px">{{ scope.row.origin }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="译文"
                width="180">
                <template slot-scope="scope">
                  <span style="margin-left: 10px">{{ scope.row.target }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                width="120">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="handleDeleteMemory(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div slot="footer" class="dialog-footer">
              <el-button @click="memorySearchResultVisible = false">关闭</el-button>
            </div>
          </el-dialog>

          <el-dialog
            title="术语库检索结果"
            :visible.sync="termSearchResultVisible"
            :modal="false"
            width="60%"
            top="5vh"
            custom-class="search-result-dialog">
              <el-descriptions 
                v-for="(item,index) in termSearchResults" 
                :key="index"
                :column="1"
                style="margin-bottom: 50px;"
                border
                size="medium"
                class="result-item">
                <el-descriptions-item label="原文" label-class-name="text-label narrow-first-column">
                  <div class="fixed-text-box">{{ item.origin }}</div>
                </el-descriptions-item>
                <el-descriptions-item label="译文" label-class-name="text-label">
                  <div class="fixed-text-box">{{ item.target }}</div>
                </el-descriptions-item>
                <el-descriptions-item label="注释" label-class-name="text-label">
                  <div class="fixed-text-box">{{ item.description }}</div>
                </el-descriptions-item>
              </el-descriptions>

              <h3>查看和修改</h3>
              <el-table
              :data="this.termSearchResults"
              style="width: 100%">
              <el-table-column
                label="原文"
                width="180">
                <template slot-scope="scope">
                  <span style="margin-left: 10px">{{ scope.row.origin }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="译文"
                width="180">
                <template slot-scope="scope">
                  <span style="margin-left: 10px">{{ scope.row.target }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="注释"
                width="180">
                <template slot-scope="scope">
                  <span style="margin-left: 10px">{{ scope.row.description }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                width="120">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="handleDeleteTerm(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div slot="footer" class="dialog-footer">
              <el-button @click="termSearchResultVisible = false">关闭</el-button>
            </div>
          </el-dialog>

          <el-dialog
            title="添加翻译对到记忆库"
            :visible.sync="memoryAddVisible"
            :modal="false"
            width="60%"
            top="5vh"
            custom-class="search-result-dialog">
              <el-form :model="inputMemory" label-width="100px">
                <el-form-item label="原文">
                  <el-input type="textarea" v-model="inputMemory.origin" :rows="2"></el-input>
                </el-form-item>
                <el-form-item label="译文">
                  <el-input type="textarea" v-model="inputMemory.target" :rows="2"></el-input>
                </el-form-item>
              </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="submitAddMemory">提交</el-button>
            </div>
          </el-dialog>

          <el-dialog
            title="添加术语到术语库"
            :visible.sync="termAddVisible"
            :modal="false"
            width="60%"
            top="5vh"
            custom-class="search-result-dialog">
              <el-form :model="inputMemory" label-width="100px">
                <el-form-item label="原文">
                  <el-input type="textarea" v-model="inputTerm.origin" :rows="2"></el-input>
                </el-form-item>
                <el-form-item label="译文">
                  <el-input type="textarea" v-model="inputTerm.target" :rows="2"></el-input>
                </el-form-item>
                <el-form-item label="注释">
                  <el-input type="textarea" v-model="inputTerm.description" :rows="2"></el-input>
                </el-form-item>
              </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="submitAddTerm">提交</el-button>
            </div>
          </el-dialog>

          <el-form :model="editForm" label-width="100px">
            <el-form-item label="段号">
              <el-input v-model="editForm.id" disabled></el-input>
            </el-form-item>
            <el-form-item label="原文">
              <el-input type="textarea" v-model="editForm.origin" :rows="9"></el-input>
            </el-form-item>
            <el-form-item label="译文">
              <el-input type="textarea" v-model="editForm.target" :rows="9"></el-input>
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
            <template slot-scope="scope">
              <div>
                <template v-for="(segment, index) in processText(scope.row.origin)">
                  <el-popover
                    v-if="segment.isTerm"
                    :key="index"
                    placement="top"
                    trigger="hover"
                    width="250">
                    <div class="term-info-card">
                      <div class="term-info-item">
                        <div class="term-info-label">译文</div>
                        <div class="term-info-content">{{ segment.term.target }}</div>
                      </div>
                      <div v-if="segment.term.description" class="term-info-item">
                        <div class="term-info-label">注释</div>
                        <div class="term-info-content">{{ segment.term.description }}</div>
                      </div>
                    </div>
                    <span slot="reference" class="term-highlight">{{ segment.text }}</span>
                  </el-popover>
                  <el-popover
                    v-else-if="segment.isMemory"
                    :key="index"
                    placement="top"
                    trigger="hover"
                    width="250">
                    <div class="term-info-card">
                      <div class="term-info-item">
                        <div class="term-info-label">记忆库译文</div>
                        <div class="term-info-content">{{ segment.memory.target }}</div>
                        <div class="copy-buttons-container">
                          <el-button 
                            size="mini" 
                            type="text" 
                            icon="el-icon-document-copy"
                            class="copy-button copy-source"
                            @click="copyToClipboard(segment.memory.origin)">
                            复制原文
                          </el-button>
                          <el-button 
                            size="mini" 
                            type="text" 
                            icon="el-icon-document-copy"
                            class="copy-button copy-target"
                            @click="copyToClipboard(segment.memory.target)">
                            复制译文
                          </el-button>
                        </div>
                      </div>
                    </div>
                    <span slot="reference" class="memory-highlight">{{ segment.text }}</span>
                  </el-popover>
                  <span v-else :key="index">{{ segment.text }}</span>
                </template>
              </div>
            </template>
            </el-table-column>
            <el-table-column
            prop="target"
            label="译文"
            width="500">
            <template slot-scope="scope">
              <div>
                <template v-for="(segment, index) in processText(scope.row.target)">
                  <el-popover
                    v-if="segment.isTerm"
                    :key="index"
                    placement="top"
                    trigger="hover"
                    width="250">
                    <div class="term-info-card">
                      <div class="term-info-item">
                        <div class="term-info-label">译文</div>
                        <div class="term-info-content">{{ segment.term.target }}</div>
                      </div>
                      <div v-if="segment.term.description" class="term-info-item">
                        <div class="term-info-label">注释</div>
                        <div class="term-info-content">{{ segment.term.description }}</div>
                      </div>
                    </div>
                    <span slot="reference" class="term-highlight">{{ segment.text }}</span>
                  </el-popover>
                  <span v-else :key="index">{{ segment.text }}</span>
                </template>
              </div>
            </template>
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
                <el-row>
                    <el-button type="success" icon="el-icon-check" @click="handleSave()">保存</el-button>
                </el-row>
                <el-row>
                    <el-button type="info" icon="el-icon-cpu" @click="handleTranslate(scope.row)">机翻</el-button>
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

      handleTermEdit(row){
        row.isEdit=true;
      },

      handleTermUpdate(row){
        this.inputTerm.origin=row.origin;
        this.inputTerm.target=row.target;
        this.inputTerm.description=row.description;
        this.submitAddTerm();
        row.isEdit=false;
      },

      handleMemoryEdit(row){
        row.isEdit=true;
      },

      handleMemoryUpdate(row){
        this.inputMemory.origin=row.origin;
        this.inputMemory.target=row.target;
        this.inputMemory.description=row.description;
        this.submitAddMemory();
        row.isEdit=false;
      },

      handleSave() {
        this.editForm.projectId = this.$store.getters.getSelectedPrjId;
        this.editForm.projectName = this.$store.getters.getSelectedPrjName;

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
        this.$router.push('/project')
      },

      querySearch(queryString, cb) {
        var restaurants = this.restaurants;
        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },

      loadAll() {
        return [];
        //return [{'value':'terminology','label':'术语库'},{'value':'memory','label':'记忆库'}];
      },
      handleSelect(item) {
        console.log(item);
      },

      searchMemory(){
        if(this.state1===''){
          this.$message.warning('请输入关键字进行搜索');
          return;
        }
        
        this.memorySearchLoading = true;
        axios.get(this.HOST+"/memory/", {
          params: {
            origin: this.state1,
            projectId: this.$store.getters.getSelectedPrjId,
          },
          headers:this.headers
        }).then(response => {
          this.memorySearchResults = response.data.memoryData.map(item => ({
            origin: item.origin,
            target: item.target
          }));
          this.memorySearchResultVisible = true;
        }).catch(error => {
          this.$message.error('检索失败: ' + error.message);
        }).finally(() => {
          this.memorySearchLoading = false;
        });
      },

      searchTerm(){
        if(this.state2===''){
          this.$message.warning('请输入关键字进行搜索');
          return;
        }
        
        this.termSearchLoading = true;
        axios.get(this.HOST+"/term/", {
          params: {
            origin: this.state2,
            projectId: this.$store.getters.getSelectedPrjId,
          },
          headers:this.headers
        }).then(response => {
          this.termSearchResults = response.data.termData.map(item => ({
            origin: item.origin,
            target: item.target,
            description: item.description
          }));
          this.termSearchResultVisible = true;
        }).catch(error => {
          this.$message.error('检索失败: ' + error.message);
        }).finally(() => {
          this.termSearchLoading = false;
        });
      },

      handleAddMemory(){
        this.memoryAddVisible = true;
      },

      handleAddTerm(){
        this.termAddVisible = true;
      },
      
      submitAddMemory(){
        if(this.inputMemory.origin==='' || this.inputMemory.target===''){
          this.$message.warning('请输入记忆库内容');
          return;
        }
        // 更新服务器数据
        this.inputMemory.projectId = this.$store.getters.getSelectedPrjId;
        axios.post(this.HOST+'/memory/', this.inputMemory).then(response => {
          this.$message.success(response.data.message);
          this.memoryAddVisible = false;
        })
        .catch(error => {
          this.$message.error('保存失败: ' + error.message);
        });
      },

      submitAddTerm(){
        if(this.inputTerm.origin==='' || this.inputTerm.target===''){
          this.$message.warning('请输入记忆库内容');
          return;
        }
        // 更新服务器数据
        this.inputTerm.projectId = this.$store.getters.getSelectedPrjId;
        axios.post(this.HOST+'/term/', this.inputTerm).then(response => {
          this.$message.success(response.data.message);
          this.termAddVisible = false;
        })
        .catch(error => {
          this.$message.error('保存失败: ' + error.message);
        });
      },

      fetchAllTerminology() {
        axios.get(this.HOST + '/getAllTerminology/', {
          params: {
            projectId: this.$store.getters.getSelectedPrjId,
          },
          headers: this.headers
        }).then(response => {
          this.allTerminology = response.data.termData;
        }).catch(error => {
          this.$message.error('获取术语库失败: ' + error.message);
        });
      },

      fetchAllMemory() {
        axios.get(this.HOST + '/getAllMemory/', {
          params: {
            projectId: this.$store.getters.getSelectedPrjId,
          },
          headers: this.headers
        }).then(response => {
          this.allMemory = response.data.memoryData;
        }).catch(error => {
          this.$message.error('获取记忆库失败: ' + error.message);
        });
      },

      processText(text) {
        if (!text) return [{text: '', isTerm: false, isMemory: false}];
        
        let segments = [];
        let lastIndex = 0;
        let matches = [];
        
        // 收集所有术语匹配
        this.allTerminology.forEach(term => {
          const regex = new RegExp(term.origin, 'gi');
          let match;
          while ((match = regex.exec(text)) !== null) {
            matches.push({
              index: match.index,
              length: match[0].length,
              text: match[0],
              type: 'term',
              data: term
            });
          }
        });

        // 收集所有记忆库匹配
        this.allMemory.forEach(memory => {
          const regex = new RegExp(memory.origin, 'gi');
          let match;
          while ((match = regex.exec(text)) !== null) {
            matches.push({
              index: match.index,
              length: match[0].length,
              text: match[0],
              type: 'memory',
              data: memory
            });
          }
        });

        // 按位置排序
        matches.sort((a, b) => a.index - b.index);

        // 处理重叠
        for (let i = matches.length - 1; i > 0; i--) {
          if (matches[i].index < matches[i-1].index + matches[i-1].length) {
            matches.splice(i, 1);
          }
        }

        // 生成段落
        lastIndex = 0;
        matches.forEach(match => {
          // 添加匹配前的普通文本
          if (match.index > lastIndex) {
            segments.push({
              text: text.slice(lastIndex, match.index),
              isTerm: false,
              isMemory: false
            });
          }
          
          // 添加匹配的文本
          segments.push({
            text: match.text,
            isTerm: match.type === 'term',
            isMemory: match.type === 'memory',
            term: match.type === 'term' ? match.data : null,
            memory: match.type === 'memory' ? match.data : null
          });
          
          lastIndex = match.index + match.length;
        });
        
        // 添加剩余文本
        if (lastIndex < text.length) {
          segments.push({
            text: text.slice(lastIndex),
            isTerm: false,
            isMemory: false
          });
        }
        
        return segments;
      },

      // 添加复制到剪贴板的方法
      copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
          this.$message({
            message: '已复制到剪贴板',
            type: 'success',
            duration: 1500
          });
        }).catch(() => {
          this.$message.error('复制失败，请重试');
        });
      },

      // 添加删除记忆库条目的方法
      handleDeleteMemory(row) {
        this.$confirm('确认删除该记忆库条目吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(this.HOST + '/deleteMemory/', {
            projectId: this.$store.getters.getSelectedPrjId,
            origin: row.origin
          }).then(response => {
            this.$message.success(response.data.message);
            // 从列表中移除该条目
            const index = this.memorySearchResults.findIndex(item => item.origin === row.origin);
            if (index > -1) {
              this.memorySearchResults.splice(index, 1);
            }
            // 重新获取所有记忆库内容以更新高亮显示
            this.fetchAllMemory();
          }).catch(error => {
            this.$message.error(error.response?.data?.message || '删除失败');
          });
        }).catch(() => {
          this.$message.info('已取消删除');
        });
      },

      // 添加删除术语库条目的方法
      handleDeleteTerm(row) {
        this.$confirm('确认删除该术语库条目吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post(this.HOST + '/deleteTerm/', {
            projectId: this.$store.getters.getSelectedPrjId,
            origin: row.origin
          }).then(response => {
            this.$message.success(response.data.message);
            // 从列表中移除该条目
            const index = this.termSearchResults.findIndex(item => item.origin === row.origin);
            if (index > -1) {
              this.termSearchResults.splice(index, 1);
            }
            // 重新获取所有术语库内容以更新高亮显示
            this.fetchAllTerminology();
          }).catch(error => {
            this.$message.error(error.response?.data?.message || '删除失败');
          });
        }).catch(() => {
          this.$message.info('已取消删除');
        });
      },
    },
    
    data() {
      return {
        restaurants: [],
        state1: '',
        state2: '',
        inputMemory: {
          origin: '',
          target: '',
          projectId:0
        },
        inputTerm:{
          origin:'',
          target:'',
          description:'',
          projectId:0
        },
        tableData: [],
        url: this.HOST+'/translate/',
        dialogVisible: false,
        editForm: {
          projectId:0,
          projectName:'',
          id: '',
          direction: '',
          origin: '',
          target: '',
          notes: ''
        },
        editIndex: -1,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        memorySearchResultVisible: false,
        memoryAddVisible : false,
        memorySearchResults: [],
        memorySearchLoading: false,

        termSearchResultVisible:false,
        termAddVisible: false,
        termSearchResults:[],
        termSearchLoading:false,
        allTerminology: [],
        allMemory: [],
      }
    },
    mounted(){
        axios.get(this.url,{
          params:{
            projectId:JSON.parse(sessionStorage.getItem('store')).selectedPrjId
          }
        }).then(response => {
            this.tableData = response.data.text;
            this.fetchAllTerminology();
            this.fetchAllMemory();
        })

        this.restaurants = this.loadAll();
    },

    created(){
      // 页面加载时，从sessionStorage中恢复状态
      if(sessionStorage.getItem('store')){
        this.$store.replaceState(
          Object.assign(
            {},
            this.$store.state,
            JSON.parse(sessionStorage.getItem('store'))
          )
        )
      }
      // 监听页面卸载事件，保存状态到sessionStorage中
      window.addEventListener('beforeunload',()=>{
        sessionStorage.setItem('store',JSON.stringify(this.$store.state))
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

.search-result-dialog {
  .el-dialog__body {
    padding: 10px 20px;
    max-height: 70vh;
    overflow-y: auto;
  }
  .text-content {
    white-space: pre-wrap;
    line-height: 1.6;
    padding: 5px;
  }
  .el-table {
    margin: 10px 0;
    .cell {
      padding: 8px 0;
    }
  }
  .dialog-footer {
    text-align: center;
    padding-top: 10px;
  }
  .narrow-first-column {
    width: 10%; /* 设置第一列的宽度为20% */
  }

  .fixed-text-box {
    word-break: break-word; /* 防止文本溢出 */
    white-space: pre-wrap; /* 保留空白符序列，并允许文本自动换行 */
  }

  .dialog-footer {
    text-align: right; /* 将关闭按钮对齐到右侧 */
  }
}

.el-table .cell span {
    padding: 2px 4px;
    border-radius: 3px;
    margin: 0 2px;
}

.term-highlight {
    background-color: #87CEFA;  /* Light Sky Blue */
    padding: 2px 4px;
    border-radius: 3px;
    margin: 0 2px;
    cursor: pointer;
}

.memory-highlight {
    color: #DAA520;  /* Golden Rod */
    font-weight: bold;
    cursor: pointer;
}

.term-info-card {
    padding: 8px;
}

.term-info-item {
    margin-bottom: 8px;
}

.term-info-item:last-child {
    margin-bottom: 0;
}

.term-info-label {
    font-size: 13px;
    color: #909399;
    margin-bottom: 4px;
}

.term-info-content {
    font-size: 14px;
    color: #303133;
    line-height: 1.4;
    word-break: break-word;
}

.term-popover {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.copy-buttons-container {
    display: flex;
    gap: 15px;
    margin-top: 8px;
}

.copy-button {
    padding: 0;
}

.copy-source {
    color: #67C23A;  /* Element UI 的成功绿色 */
}

.copy-source:hover {
    color: #85ce61;
}

.copy-target {
    color: #409EFF;  /* Element UI 的主题蓝色 */
}

.copy-target:hover {
    color: #66b1ff;
}
</style>