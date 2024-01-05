import { PlaywrightCrawler, RequestQueue, log, Dataset, ProxyConfiguration  } from 'crawlee';
import { router } from './routes.mjs';

log.setLevel(log.LEVELS.INFO);
log.debug('Setting up crawler.');
const proxyConfiguration = new ProxyConfiguration({
    proxyUrls: [
        'http://172.16.3.128:7889',
    ],
});
for (let year = 22; year <= 23; year++) {
    for (let month = 1; month <= 12; month++) {
        const yearMonth = year.toString().padStart(2, '0') + month.toString().padStart(2, '0');
        const requestQueue = await RequestQueue.open();
        
        // 为每个月生成 URL
        for (let paper = 1; paper <= 1; paper++) {
            const paperNumber = paper.toString().padStart(5, '0');
            const url = `https://arxiv.org/abs/${yearMonth}.${paperNumber}`;
            await requestQueue.addRequest({ url });
        }

        // 初始化并运行爬虫
        const crawler = new PlaywrightCrawler({
            proxyConfiguration,
            requestHandler: router,
            maxRequestsPerCrawl: 1000,
            maxRequestRetries: 5,
            requestQueue,
        });

        await crawler.run();
        
        // 每个月爬取结束后存储数据
        await Dataset.exportToJSON(`arxiv_${yearMonth}`);
        // await Dataset.exportToCSV(`arxiv_${yearMonth}`);

        // 清空或关闭当前的 RequestQueue
        await requestQueue.drop();
    }
}
