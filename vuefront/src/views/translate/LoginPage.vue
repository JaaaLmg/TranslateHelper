<template>
  <div class="app-container">
    <header class="app-header">
      <div class="auth-switch">
        <h1 
          class="app-title" 
          :class="{ 'active': !isRegister }"
          @click="isRegister = false"
        >用户登录</h1>
        <span class="divider">/</span>
        <h1 
          class="app-title" 
          :class="{ 'active': isRegister }"
          @click="isRegister = true"
        >用户注册</h1>
      </div>
      <p class="app-subtitle">欢迎使用翻译助手</p>
    </header>
    <main class="app-main">
      <form class="login-form" @submit.prevent="handleSubmit">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <div v-if="success" class="success-message">
          {{ success }}
        </div>
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="form.username" placeholder="请输入用户名" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="form.password" placeholder="请输入密码" required>
        </div>
        <div v-if="isRegister" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input type="password" id="confirmPassword" v-model="form.confirmPassword" placeholder="请再次输入密码" required>
        </div>
        <button type="submit" class="btn-start" :disabled="isLoading">
          <span v-if="!isLoading">{{ isRegister ? '注册' : '登录' }}</span>
          <span v-else>{{ isRegister ? '注册中...' : '登录中...' }}</span>
        </button>
      </form>
    </main>
  </div>
</template>

<style>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.app-header {
  text-align: center;
  margin-bottom: 3rem;
}

.app-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
}

.auth-switch {
  display: flex;
  align-items: center;
  gap: 10px;
}

.auth-switch .app-title {
  cursor: pointer;
  margin: 0;
  position: relative;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.auth-switch .app-title.active {
  opacity: 1;
}

.auth-switch .app-title.active::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: #3498db;
  border-radius: 3px;
}

.divider {
  color: #7f8c8d;
  font-size: 2rem;
}

.app-subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.login-form {
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-size: 1rem;
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn-start {
  width: 100%;
  padding: 1rem;
  font-size: 1.2rem;
  color: white;
  background-color: #3498db;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-start:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.btn-start:active {
  transform: translateY(0);
}

.btn-start:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 4px;
  text-align: center;
}

.success-message {
  color: #2ecc71;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: rgba(46, 204, 113, 0.1);
  border-radius: 4px;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

@media (max-width: 768px) {
  .app-title {
    font-size: 2rem;
  }
  .app-subtitle {
    font-size: 1rem;
  }
  .login-form {
    max-width: 350px;
  }
}

@media (max-width: 480px) {
  .app-container {
    padding: 1rem;
  }
  .app-title {
    font-size: 1.5rem;
  }
  .app-subtitle {
    font-size: 0.9rem;
  }
  .login-form {
    max-width: 300px;
  }
}
</style>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      error: '',
      success: '',
      isLoading: false,
      isRegister: false
    }
  },
  methods: {
    async handleSubmit() {
      if (!this.validateForm()) return;
      
      this.isLoading = true;
      try {
        const endpoint = this.isRegister ? '/register/' : '/login/';
        const response = await fetch(this.HOST + endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.form.username,
            password: this.form.password
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          // 优先显示后端返回的error字段，其次显示message字段，最后使用默认提示
          throw new Error(errorData.error || errorData.message || this.isRegister ? '注册失败' : '登录失败，请检查用户名和密码');
        }

        if (this.isRegister) {
          this.success = '注册成功！';
          // 清空表单
          this.form = {
            username: '',
            password: '',
            confirmPassword: ''
          };
          // 自动切换回登录状态
          setTimeout(() => {
            this.isRegister = false;
            this.success = '';
          }, 2000);
        } else {
          // 登录成功后跳转
          this.$router.push('/project');
        }
      } catch (error) {
        this.error = error.message || '请求失败，请检查网络连接后重试';
      } finally {
        this.isLoading = false;
      }
    },
    validateForm() {
      if (!this.form.username.trim()) {
        this.error = '请输入用户名';
        return false;
      }
      if (!this.form.password) {
        this.error = '请输入密码';
        return false;
      }
      if (this.isRegister && this.form.password !== this.form.confirmPassword) {
        this.error = '两次输入的密码不一致';
        return false;
      }
      this.error = '';
      return true;
    }
  }
}
</script>
