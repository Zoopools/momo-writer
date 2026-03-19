#!/usr/bin/env bun

import { tryConnectExisting, sleep, clickElement } from './cdp.ts';

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

  console.log('[publish] Found WeChat tab');

  // 连接到 tab
  const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

  await cdp.send('Runtime.enable', {}, { sessionId });
  await cdp.send('DOM.enable', {}, { sessionId });

  const session = { cdp, sessionId, targetId: wechatTarget.targetId };

  // 点击发表按钮
  console.log('[publish] Clicking publish button...');
  
  try {
    await clickElement(session, '.mass_send');
    console.log('[publish] Publish button clicked!');
    
    await sleep(2000);
    
    console.log('[publish] Waiting for user to confirm...');
    console.log('[publish] A dialog should appear. Please confirm the publish action.');
  } catch (error) {
    console.error('[publish] Error clicking publish button:', error);
    console.log('[publish] Please click the publish button manually.');
  }
}

main().catch(console.error);