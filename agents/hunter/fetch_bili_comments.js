#!/usr/bin/env node

const https = require('https');
const fs = require('fs');

const AID = '116141955481993';

function fetchPage(pn) {
  return new Promise((resolve, reject) => {
    const url = `https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=${pn}&oid=${AID}&type=1&sort=2&ps=20`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.data.replies || []);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  console.log('开始抓取前 100 条热评...');
  const allComments = [];
  
  for (let i = 1; i <= 5; i++) {
    console.log(`抓取第 ${i} 页...`);
    const replies = await fetchPage(i);
    for (const reply of replies) {
      const imgSrc = reply.content.pictures && reply.content.pictures[0] ? reply.content.pictures[0].img_src : '';
      allComments.push({
        commenter: reply.member.uname,
        content: reply.content.message.replace(/\n/g, ' '),
        likes: reply.like,
        ctime: reply.ctime * 1000,
        image: imgSrc
      });
    }
  }
  
  console.log(`\n共抓取 ${allComments.length} 条评论`);
  
  // 输出 JSON 格式供后续使用
  const output = {
    total: allComments.length,
    comments: allComments
  };
  
  fs.writeFileSync('/tmp/bili_comments_100.json', JSON.stringify(output, null, 2));
  console.log('数据已保存到 /tmp/bili_comments_100.json');
  
  // 显示前 10 条预览
  console.log('\n前 10 条预览:');
  allComments.slice(0, 10).forEach((c, i) => {
    console.log(`${i+1}. ${c.commenter}: ${c.content.substring(0, 40)}... (${c.likes}赞) ${c.image ? '[有图]' : ''}`);
  });
}

main().catch(console.error);
