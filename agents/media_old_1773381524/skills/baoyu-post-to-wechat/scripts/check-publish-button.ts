#!/usr/bin/env bun

import { tryConnectExisting, sleep, evaluate } from './cdp.ts';

async function main() {
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

  console.log('[publish] Found WeChat tab:', wechatTarget.url);

  // 连接到 tab
  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

  await cdp.send('Runtime.enable', {}, { sessionId });

  // 检查页面状态
  const pageInfo = await evaluate({ cdp, sessionId, targetId: wechatTarget.targetId }, `
    (function() {
      const url = window.location.href;
      const title = document.title;
      const buttons = Array.from(document.querySelectorAll('button'))
        .filter(b => b.offsetParent !== null)
        .map(b => ({ text: b.textContent, class: b.className }))
        .slice(0, 10);
      return JSON.stringify({ url, title, buttons });
    })()
  `);

  console.log('[publish] Page info:', pageInfo);

  // 查找发表按钮
  const buttonCheck = await evaluate({ cdp, sessionId, targetId: wechatTarget.targetId }, `
    (function() {
      // 常见的发表按钮选择器
      const selectors = [
        '.weui-desktop-btn_publish',
        '[data-e2e="btn-publish"]',
        'button.weui-desktop-btn__primary'
      ];

      for (const selector of selectors) {
        const btn = document.querySelector(selector);
        if (btn && btn.offsetParent !== null) {
          return JSON.stringify({ found: true, selector, text: btn.textContent });
        }
      }

      return JSON.stringify({ found: false, message: 'Publish button not found in current view' });
    })()
  `);

  console.log('[publish] Button check:', buttonCheck);

  if (buttonCheck.found) {
    console.log('[publish] Found publish button! Ready to publish.');
  } else {
    console.log('[publish] Publish button not found. User may need to navigate to the editor first.');
  }
}

main().catch(console.error);