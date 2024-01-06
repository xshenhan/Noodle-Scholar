import { CrawlerExtension, createPlaywrightRouter, Dataset } from 'crawlee';
import axios from 'axios';
// createPlaywrightRouter() is only a helper to get better
// intellisense and typings. You can use Router.create() too.
export const router = createPlaywrightRouter();

function extractIdFromUrl(url) {
    var match = url.match(/https:\/\/arxiv\.org\/abs\/(.*)/);
    return match ? match[1] : null;
}

function extractSubmitter(str) {
    var regex = /From:\s*(.+?)\s*\[/;
    var match = str.match(regex);
    return match ? match[1] : null;
}

function extractSubject(str) {
    var regex = /\((.*?)\)/g;
    var matches = [];
    var match;

    while (match = regex.exec(str)) {
        matches.push(match[1]);
    }

    return matches;
}

// This replaces the request.label === DETAIL branch of the if clause.
async function safeEval(page, selector, pageFunction) {
    const element = await page.$(selector);
    if (element) {
        return page.$eval(selector, pageFunction);
    } else {
        return null;
    }
}

async function safeEvalAll(page, selector, pageFunction) {
    const elements = await page.$$(selector);
    if (elements.length > 0) {
        return page.$$eval(selector, pageFunction);
    } else {
        return null;
    }
}


router.addHandler('DETAIL', async ({ request, page, log }) => {
    log.info(`Extracting data: ${request.url}`);
    const id = extractIdFromUrl(request.url);
    const title = await safeEval(page, 'h1.title', h1 => h1.innerText);
    const submitter = extractSubmitter(await safeEval(page, 'div.submission-history', div => div.innerText));
    const authorElements = await safeEvalAll(page, 'div.authors > a', (as) => as.map(a => a.innerText));
    const authors = authorElements.join(', '); // Authors as a single string separated by spaces
    const comments = await safeEval(page, 'td.comments', div => div.innerText);
    const abstract = await safeEval(page, 'blockquote.abstract', div => div.innerText);
    const categoryElements = extractSubject(await safeEval(page, 'td.subjects', td => td.innerText));
    const categories = categoryElements.join(' '); // Categories as a single string
    const license = await safeEval(page, 'div.abs-license > a', a => a.href);
    const dateStr = await safeEval(page, 'div.dateline', div => div.innerText); // '[Submitted on 2 Nov 2023]'
    const dateMatch = dateStr.match(/(\d{1,2})\s(\w+)\s(\d{4})/);
    const date = dateMatch ? `${dateMatch[3]}-${monthToNumber(dateMatch[2])}-${dateMatch[1].padStart(2, '0')}` : null;
    const doiLink = await safeEval(page, 'td.arxivdoi > a', a => a.href); // 获取DOI链接
    const doi = doiLink.split('/').pop(); // 从DOI链接中提取DOI
    const journalRef = await safeEval(page, 'td.journal-ref', td => td.innerText); // 提取journal reference
    const year = parseInt(id.substring(0, 2), 10) + 2000; // 从arxiv_id提取年份

    const data = {
        id,
        title,
        submitter,
        authors,
        author:authorElements,
        comments,
        abstract,
        categories,
        license,
        date,
        doi, // Updated DOI
        journalRef, // Added journal reference
        year // Added year
    };

    // print data for debugging
    log.debug(id);
    log.debug(title);
    log.debug(submitter);
    log.debug(authors);
    await Dataset.pushData(data);

    function monthToNumber(monthName) {
        const months = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        };
        return months[monthName] || '00';
    }

});

router.addHandler('CATEGORY', async ({ page, enqueueLinks, request, log }) => {
    log.info(`In: ${request.url}`);
    await enqueueLinks({
        selector: "a[title='Abstract']",
        label: 'DETAIL'
    });
});

router.addDefaultHandler(async ({ request, page, enqueueLinks, log }) => {
    log.info(`In: ${request.url}`);
    
    // 检查URL格式是否正确，如果不是目标格式则跳过处理
    const urlMatch = request.url.match(/https:\/\/arxiv.org\/abs\/(\d{4}\.\d{5})/);
    if (!urlMatch) {
        log.info(`Skipping non-target URL: ${request.url}`);
        return;
    }

    // 从URL中提取年份和月份
    const yearMonth = urlMatch[1].substring(0, 4);
    const year = yearMonth.substring(0, 2);
    const month = yearMonth.substring(2, 4);

    // 生成当月所有目标文章的URL
    const urls = [];
    for (let paper = 1; paper <= 1000; paper++) {
        const paperNumber = paper.toString().padStart(5, '0');
        const url = `https://arxiv.org/abs/${yearMonth}.${paperNumber}`;
        urls.push(url);
    }
    log.info(`Generated ${urls.length} URLs for ${yearMonth}`);
    log.info(`First URL: ${urls[0]}`);
    // 将生成的URL添加到爬取队列
    await enqueueLinks({
        urls: urls,
        label: 'DETAIL', // 标记为详细页处理
    });
});
