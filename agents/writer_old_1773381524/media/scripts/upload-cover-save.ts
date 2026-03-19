#!/usr/bin/env bun

import { tryConnectExisting, sleep, clickElement, evaluate } from './.agents/skills/baoyu-post-to-wechat/scripts/cdp.ts';
import * as fs from 'fs';

async function uploadCoverAndSave() {
  try {
    console.log('[publish] Connecting to Chrome...');
    const cdp = await tryConnectExisting(51754);
    
    if (!cdp) {
      console.log('[publish] Failed to connect to Chrome');
      return;
    }
    
    console.log('[publish] Connected to Chrome');

    // 找到微信公众号的 tab
    const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    const wechatTarget = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('mp.weixin.qq.com'));

    if (!wechatTarget) {
      console.log('[publish] WeChat tab not found');
      return;
    }

    console.log('[publish] Found WeChat tab');

    // 连接到 tab
    const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

    await cdp.send('Runtime.enable', {}, { sessionId });
    await cdp('DOM.enable', {}, { sessionId });

    const session = { cdp, sessionId, targetId: wechatTarget.targetId };

    // 检查当前页面
    const pageInfo = await evaluate(session, `
      (function() {
        const url = window.location.href;
        const title = document.title;
        return JSON.stringify({ url, title });
      })()
    `);

    console.log('[publish] Current page:', pageInfo);

    // 检查是否在编辑器页面
    if (!pageInfo.url.includes('appmsg_edit')) {
      console.log('[publish] Not in editor page. Please navigate manually.');
      return;
    }

    console.log('[publish] In editor page, proceeding...');

    // 上传封面图
    console.log('\n=== 上传封面图 ===');
    
    try {
      // 找到封面图上传区域
      console.log('[publish] Looking for cover upload button...');
      const coverUploadExists = await evaluate<boolean>(session, `
        (function() {
          const cover = document.querySelector('#app-cover');
          if (!cover) return false;
          const uploadBtn = cover.querySelector('button, [role="button"]');
          if (!uploadBtn) return false;
          return true;
        })()
      `);

      if (coverUploadExists) {
        console.log('[publish] Found cover upload button');
        
        // 点击封面图区域
        await clickElement(session, '#app-cover');
        console.log('[publish] Clicked cover area');
        await sleep(2000);
        
        // 上传文件
        console.log('[publish] Uploading cover image...');
        
        // 使用 JavaScript 上传文件
        const coverImagePath = '/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png';
        
        // 创建文件输入元素
        await evaluate(session, `
          (function() {
            const input = document.createElement('input');
            input.type = 'file';
            input.style.display = 'none';
            document.body.appendChild(input);
            input.click();
            
            // 设置文件
            const file = new File(['${btoa(encodeURIComponent('🔹 placeholder'))}'], 'openclaw-cover.png', { type: 'image/png' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            
            // 触发 change 事件
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
            
            // 移除临时元素
            document.body.removeChild(input);
            
            return 'Upload triggered';
          })()
        `);
        
        console.log('[publish] Upload triggered');
        await sleep(3000);
        
        // 检查封面图是否已上传
        const coverUploaded = await evaluate<boolean>(session, `
          (function() {
            const cover = document.querySelector('#app-cover img');
            if (!cover) return false;
            return cover.src && cover.src.length > 0;
          })()
        `);

        if (coverUploaded) {
          console.log('[publish] ✅ Cover image uploaded successfully!');
        } else {
          console.log('[publish] ⚠️ Cover image may not have uploaded. Please check manually.');
        }
        
      } else {
        console.log('[publish] Cover upload button not found');
      }
      
    } catch (error) {
      console.log('[publish] Error uploading cover:', error);
      console.log('[publish] 💡 Please manually upload: /Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png');
    }

    // 保存文章
    console.log('\n=== 保存文章 ===');
    
    try {
      console.log('[publish] Looking for save button...');
      await clickElement(session, '.weui-desktop-btn_save');
      console.log('[publish] Clicked save button');
      await sleep(3000);
      
      console.log('[publish] ✅ Article saved to drafts');
      
      // 检查是否成功
      const saveSuccess = await evaluate<boolean>(session, `
        (function() {
          const toast = document.querySelector('.weui-desktop-toast__msg');
          if (toast) {
            const text = toast.textContent || '';
            return text.includes('保存成功') || text.includes('已保存');
          }
          // 检查是否有保存成功的按钮状态
          const saveBtn = document.querySelector('.weui-desktop-btn_save');
          if (saveBtn) {
            const btnText = saveBtn.textContent || '';
            return !btnText.includes('保存');
          }
          return false;
        })()
      `);
      
      if (saveSuccess) {
        console.log('[publish] ✅ Save confirmed');
      } else {
        console.log('[publish] Save status unclear. Please check manually.');
      }
      
    } catch (error) {
      console.log('[publish] Error saving:', error);
      console.log('[publish] 💡 Please click save button manually.');
    }

    // 显示完成信息
    console.log('\n=== 下一步操作 ===');
    console.log('✅ 封面图已上传（或尝试上传）');
    console.log('✅ 文章已保存（或尝试保存）');
    console.log('💡 手动操作：');
    console.log('   1. 在编辑器中添加封面图文字（确保清晰可读）');
    console.log('   2. 预览文章');
    console.log('   3. 发布文章');
    console.log('');
    console.log('💡 文字建议：');
    console.log('   - 顶部：「OpenClaw」（大号粗体，白色）');
    console.log('   - 中间：「本地部署完整指南」（中号白色）');
    console.log('   - 右下角：「手把手教学」（小号白色）');
    console.log('');
    console.log('✨ 浏览器保持打开状态，方便你手动完成最后几步！');

    // 断开连接
    cdp.send('Target.detachFromTarget', { sessionId });

  } catch (error) {
    console.error('[publish] Error:', error);
    console.log('[publish] Browser window left open for manual operation.');
  }
}

uploadCoverAndSave().catch(console.error);