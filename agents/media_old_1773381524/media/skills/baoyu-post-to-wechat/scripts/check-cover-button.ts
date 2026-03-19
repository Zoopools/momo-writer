#!/usr/bin/env bun

import { tryConnectExisting, sleep, evaluate, clickElement } from './cdp.ts';

async function addCoverImage() {
  console.log('[cover] Connecting to Chrome...');
  
  const cdp = await tryConnectExisting(51754);
  
  if (!cdp) {
    console.log('[cover] Failed to connect to Chrome');
    return;
  }
  
  console.log('[cover] Connected to Chrome');

  // 找到微信公众号的 tab
  const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
  const wechatTarget = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('mp.weixin.qq.com'));

  if (!wechatTarget) {
    console.log('[cover] WeChat tab not found');
    return;
  }

  console.log('[cover] Found WeChat tab:', wechatTarget.url);

  // 连接到 tab
  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });

  const session = { cdp, sessionId, targetId: wechatTarget.targetId };

  // 检查当前页面
  const pageInfo = await evaluate(session, `
    (function() {
      const url = window.location.href;
      const title = document.title;
      return JSON.stringify({ url, title });
    })()
  `);

  console.log('[cover] Current page:', pageInfo);

  // 查找封面图上传按钮
  const coverCheck = await evaluate(session, `
    (function() {
      // 常见的封面图选择器
      const selectors = [
        '#app-cover',
        '.cover-upload',
        '[data-e2e="cover"]',
        '.weui-desktop-upload__input'
      ];

      for (const selector of selectors) {
        const el = document.querySelector(selector);
        if (el && el.offsetParent !== null) {
          return JSON.stringify({ found: true, selector, tag: el.tagName });
        }
      }

      return JSON.stringify({ found: false, message: 'Cover upload button not found' });
    })()
  `);

  console.log('[cover] Cover check:', coverCheck);

  cdp.send('Target.detachFromTarget', { sessionId });
}

addCoverImage().catch(console.error);