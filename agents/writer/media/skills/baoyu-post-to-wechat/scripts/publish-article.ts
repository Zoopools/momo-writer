import { connectToExistingChrome, sleep, clickElement, evaluate } from './cdp.ts';

async function publishArticle() {
  try {
    // 连接到哥哥的浏览器
    const cdp = await connectToExistingChrome(51754);
    console.log('[publish] Connected to Chrome');

    // 找到微信公众号的 tab
    const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    const wechatTarget = targets.targetInfos.find(t => t.type === 'page' && t.url.includes('mp.weixin.qq.com'));

    if (!wechatTarget) {
      throw new Error('WeChat tab not found');
    }

    console.log('[publish] Found WeChat tab:', wechatTarget.url);

    // 连接到 tab
    const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', { targetId: wechatTarget.targetId, flatten: true });

    await cdp.send('Runtime.enable', {}, { sessionId });

    // 检查是否有发表按钮
    const hasPublishButton = await evaluate<boolean>(session, `
      (function() {
        const btn = document.querySelector('.weui-desktop-btn_publish') ||
                   document.querySelector('[data-e2e="btn-publish"]') ||
                   document.querySelector('button:contains("发表")');
        return !!btn;
      })()
    `);

    if (!hasPublishButton) {
      console.log('[publish] Publish button not found. User needs to click manually.');
      console.log('[publish] Browser window left open for manual publishing.');
      return;
    }

    // 点击发表按钮
    console.log('[publish] Clicking publish button...');
    await clickElement({ cdp, sessionId, targetId: wechatTarget.targetId }, '.weui-desktop-btn_publish');

    await sleep(2000);

    // 等待确认对话框
    console.log('[publish] Waiting for confirmation dialog...');

    // 点击确认
    try {
      await clickElement({ cdp, sessionId, targetId: wechatTarget.targetId }, '.weui-desktop-dialog__btn_primary');
      console.log('[publish] Confirmed publish!');
    } catch (e) {
      console.log('[publish] No confirmation dialog needed or already published.');
    }

    console.log('[publish] Done! Article should be published now.');

  } catch (error) {
    console.error('[publish] Error:', error);
    console.log('[publish] Browser window left open for manual publishing.');
  }
}

publishArticle();