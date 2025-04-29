<template>
    <div class="app-container">
      <header class="app-header">
        <h1 class="app-title">翻译助手</h1>
        <p class="app-subtitle">您的智能翻译解决方案</p>
      </header>
      <main class="app-main">
        <button class="btn-start" @click="redirectToLogin">开始使用</button>
        <!-- <button class="btn-start">
            <router-link to="/login">开始使用</router-link>
        </button> -->
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
  
  .app-title::after {
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
  
  .app-subtitle {
    font-size: 1.2rem;
    color: #7f8c8d;
  }
  
  .btn-start {
    padding: 1rem 2rem;
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
  
  @media (max-width: 768px) {
    .app-title {
      font-size: 2rem;
    }
    .app-subtitle {
      font-size: 1rem;
    }
    .btn-start {
      padding: 0.8rem 1.5rem;
      font-size: 1rem;
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
  }
</style>
  
<script>
  export default {
    methods: {
      redirectToLogin() {
        // window.location.href = 'http://localhost:5000/login';
        this.$router.push('/login')
      }
    }
  }
</script>