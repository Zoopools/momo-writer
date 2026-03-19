#!/usr/bin/env bun

import { tryConnectExisting, sleep, clickElement, evaluate } from './.agents/skills/baoyu-post-to-wechat/scripts/cdp.ts';

async function publishArticleWithCover() {
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
      console.log('[publish] WeChat tab not found. Opening...');
      return;
    }

    console.log('[publish] Found WeChat tab');

    // 连接到 tab
    const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

    await cdp.send('Runtime.enable', {}, { sessionId });
    await cdp.send('DOM.enable', {}, { sessionId });

    const session = { cdp, sessionId, targetId: wechatTarget.targetId };

    // 检查页面状态
    const pageInfo = await evaluate(session, `
      (function() {
        const url = window.location.href;
        const title = document.title;
        const buttons = Array.from(document.querySelectorAll('button'))
          .filter(b => b.offsetParent !== null)
          .map(b => ({ text: b.textContent.trim(), class: b.className, id: b.id }))
          .slice(0, 15);
        return JSON.stringify({ url, title, buttons });
      })()
    `);

    console.log('[publish] Current page info:', pageInfo);

    // 检查是否在编辑器页面
    if (pageInfo.url.includes('appmsg_edit')) {
      console.log('[publish] Currently in editor page');
      console.log('[publish] READY FOR MANUAL COVER UPLOAD');
      
      // 显示操作提示
      console.log('\n📋 操作步骤：');
      console.log('1. 查找封面图上传区域（通常在右上角）');
      console.log('2. 点击封面图区域');
      console.log('3. 选择文件：/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png');
      console.log('4. 等待上传完成');
      console.log('5. 在编辑器中添加标题文字（顶部大标题：OpenClaw）');
      console.log('6. 在编辑器中添加副标题（中：本地部署完整指南）');
      console.log('7. 在编辑器中添加标签（右下角小字：手把手教学）');
      console.log('8. 保存文章');
      console.log('9. 发布文章');
      console.log('\n💡 文字建议：');
      console.log('   - 使用大号粗体，白色文字');
      console.log('   - 确保高对比度');
      console.log('   - 避免文字遮挡图标');
      console.log('\n✨ 浏览器保持打开状态，方便你手动操作！');
      
    } else if (pageInfo.url.includes('cgi-bin/home')) {
      console.log('[publish] Currently on home page');
      console.log('[publish] Navigating to drafts...');
      
      // 点击草稿箱
      try {
        const draftLink = Array.from(document.querySelectorAll('a')).find(a => 
          a.textContent.includes('草稿箱') || a.href.includes('draft')
        );
        if (draftLink) {
          draftLink.click();
          await sleep(2000);
        }
      } catch (e) {
        console.log('[publish] Could not auto-navigate, please manually go to drafts');
      }
    }

    // 断开连接
    cdp.send('Target.detachFromTarget', { sessionId });

  } catch (error) {
    console.error('[publish] Error:', error);
    console.log('[publish] Browser window left open for manual operation');
  }
}

publishArticleWithCover().catch(console.error);