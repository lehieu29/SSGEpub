/**
 * Test script for URL obfuscation functionality
 * Run in browser console to verify obfuscation works
 */

// Test the obfuscation functionality
function testObfuscation() {
    console.log('🧪 Testing URL Obfuscation...');
    
    // Test URLs
    const testUrls = [
        'https://drive.google.com/file/d/1atVRKbZ07rSF5X_Q0OW1lLKywqAj4yvd/view?usp=sharing',
        'https://onedrive.live.com/download?cid=123&resid=456',
        'https://mega.nz/file/abcd1234#xyz567890'
    ];
    
    testUrls.forEach((url, index) => {
        console.log(`\n--- Test ${index + 1} ---`);
        console.log(`Original: ${url}`);
        
        // Encode
        const encoded = LinkObfuscator.encode(url);
        console.log(`Encoded: data:encoded,${encoded}`);
        
        // Decode
        const decoded = LinkObfuscator.decode(encoded);
        console.log(`Decoded: ${decoded}`);
        
        // Verify
        const isCorrect = decoded === url;
        console.log(`✅ Test ${index + 1}: ${isCorrect ? 'PASSED' : 'FAILED'}`);
        
        if (!isCorrect) {
            console.error(`❌ Mismatch detected!`);
        }
    });
    
    console.log('\n🎯 Testing API response formats...');
    
    // Test API response handling
    const testConfigs = [
        2,                              // Direct number
        { index: 1 },                   // Object with index
        { activeIndex: 0 },             // Object with activeIndex  
        { activeIndices: [2, 1, 0] }    // Legacy array format
    ];
    
    const mockLinks = [
        { platform: 'Google Drive', index: 0, url: 'https://drive.google.com/...' },
        { platform: 'OneDrive', index: 1, url: 'https://onedrive.live.com/...' },
        { platform: 'YeuMoney', index: 2, url: 'https://yeumoney.com/...' }
    ];
    
    // Create temp download manager for testing
    const tempManager = new DownloadConfigManager();
    
    testConfigs.forEach((config, index) => {
        console.log(`\nAPI Test ${index + 1}: ${JSON.stringify(config)}`);
        const result = tempManager.filterLinks(config, mockLinks);
        console.log(`Result: ${result.length} link(s) - ${result.map(l => l.platform).join(', ')}`);
    });
    
    console.log('\n✅ All tests completed!');
}

// Auto-run test if LinkObfuscator is available
if (typeof LinkObfuscator !== 'undefined') {
    testObfuscation();
} else {
    console.warn('⚠️ LinkObfuscator not loaded. Include download-config.js first.');
}

