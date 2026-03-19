#!/usr/bin/env node

const https = require('https');

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
  console.log('开始抓取 B 站评论...');
  const allComments = [];
  
  for (let i = 1; i <= 5; i++) {
    console.log(`抓取第 ${i} 页...`);
    const replies = await fetchPage(i);
    for (const reply of replies) {
      allComments.push({
        commenter: reply.member.uname,
        content: reply.content.message,
        likes: reply.like,
        ctime: reply.ctime * 1000
      });
    }
  }
  
  console.log(`\n共抓取 ${allComments.length} 条评论`);
  console.log('\nJSON 输出:');
  console.log(JSON.stringify(allComments, null, 2));
}

main().catch(console.error);
