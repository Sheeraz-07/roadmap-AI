"""
Component Search and Pricing Module
Searches for electronic components across multiple suppliers and provides cost-efficient recommendations
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Optional
import re

class ComponentSearcher:
    """Search for electronic components and pricing across multiple suppliers"""
    
    def __init__(self):
        self.suppliers = {
            'adafruit': 'https://www.adafruit.com',
            'sparkfun': 'https://www.sparkfun.com',
            'amazon': 'https://www.amazon.com',
            'aliexpress': 'https://www.aliexpress.com'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_component(self, component_name: str, component_type: str = "") -> Dict:
        """Search for a specific component across suppliers"""
        results = {
            'component_name': component_name,
            'component_type': component_type,
            'suppliers': [],
            'best_price': None,
            'recommended': None,
            'alternatives': []
        }
        
        # Search each supplier
        for supplier_name, base_url in self.suppliers.items():
            try:
                supplier_results = self._search_supplier(supplier_name, component_name)
                if supplier_results:
                    results['suppliers'].extend(supplier_results)
            except Exception as e:
                print(f"Error searching {supplier_name}: {str(e)}")
        
        # Analyze results and find best options
        if results['suppliers']:
            results['best_price'] = min(results['suppliers'], key=lambda x: x.get('price', float('inf')))
            results['recommended'] = self._get_recommended_component(results['suppliers'])
            results['alternatives'] = self._get_alternatives(results['suppliers'])
        
        return results
    
    def _search_supplier(self, supplier: str, component: str) -> List[Dict]:
        """Search a specific supplier for components"""
        if supplier == 'adafruit':
            return self._search_adafruit(component)
        elif supplier == 'sparkfun':
            return self._search_sparkfun(component)
        elif supplier == 'amazon':
            return self._search_amazon(component)
        elif supplier == 'aliexpress':
            return self._search_aliexpress(component)
        return []
    
    def _search_adafruit(self, component: str) -> List[Dict]:
        """Search Adafruit for components"""
        try:
            # Mock data for demonstration - in real implementation, scrape actual data
            mock_results = [
                {
                    'name': f'{component} - Adafruit',
                    'price': 12.95,
                    'supplier': 'Adafruit',
                    'url': f'https://www.adafruit.com/product/123',
                    'sku': 'ADA-123',
                    'in_stock': True,
                    'specifications': {
                        'voltage': '3.3V-5V',
                        'accuracy': '±0.5°C',
                        'interface': 'I2C'
                    }
                }
            ]
            return mock_results
        except Exception:
            return []
    
    def _search_sparkfun(self, component: str) -> List[Dict]:
        """Search SparkFun for components"""
        try:
            mock_results = [
                {
                    'name': f'{component} - SparkFun',
                    'price': 14.95,
                    'supplier': 'SparkFun',
                    'url': f'https://www.sparkfun.com/products/456',
                    'sku': 'SEN-456',
                    'in_stock': True,
                    'specifications': {
                        'voltage': '3.3V-5V',
                        'accuracy': '±0.3°C',
                        'interface': 'OneWire'
                    }
                }
            ]
            return mock_results
        except Exception:
            return []
    
    def _search_amazon(self, component: str) -> List[Dict]:
        """Search Amazon for components"""
        try:
            mock_results = [
                {
                    'name': f'{component} - Generic',
                    'price': 8.99,
                    'supplier': 'Amazon',
                    'url': f'https://www.amazon.com/dp/B08XYZ123',
                    'sku': 'B08XYZ123',
                    'in_stock': True,
                    'specifications': {
                        'voltage': '3.3V-5V',
                        'accuracy': '±1°C',
                        'interface': 'OneWire'
                    }
                }
            ]
            return mock_results
        except Exception:
            return []
    
    def _search_aliexpress(self, component: str) -> List[Dict]:
        """Search AliExpress for components"""
        try:
            mock_results = [
                {
                    'name': f'{component} - Budget Option',
                    'price': 3.99,
                    'supplier': 'AliExpress',
                    'url': f'https://www.aliexpress.com/item/123456789.html',
                    'sku': 'ALI-789',
                    'in_stock': True,
                    'shipping_time': '15-30 days',
                    'specifications': {
                        'voltage': '3.3V-5V',
                        'accuracy': '±2°C',
                        'interface': 'OneWire'
                    }
                }
            ]
            return mock_results
        except Exception:
            return []
    
    def _get_recommended_component(self, suppliers: List[Dict]) -> Dict:
        """Get the recommended component based on price, quality, and availability"""
        # Score components based on multiple factors
        for component in suppliers:
            score = 0
            
            # Price factor (lower is better)
            if component.get('price', 0) < 10:
                score += 3
            elif component.get('price', 0) < 20:
                score += 2
            else:
                score += 1
            
            # Supplier reliability
            if component.get('supplier') in ['Adafruit', 'SparkFun']:
                score += 3
            elif component.get('supplier') == 'Amazon':
                score += 2
            else:
                score += 1
            
            # Availability
            if component.get('in_stock'):
                score += 2
            
            component['recommendation_score'] = score
        
        return max(suppliers, key=lambda x: x.get('recommendation_score', 0))
    
    def _get_alternatives(self, suppliers: List[Dict]) -> List[Dict]:
        """Get alternative components sorted by value"""
        sorted_suppliers = sorted(suppliers, key=lambda x: x.get('price', float('inf')))
        return sorted_suppliers[:3]  # Return top 3 alternatives
    
    def get_cost_analysis(self, components: List[str]) -> Dict:
        """Analyze total project cost and suggest cost-efficient alternatives"""
        total_cost = 0
        budget_alternatives = []
        premium_options = []
        
        for component in components:
            search_result = self.search_component(component)
            if search_result['best_price']:
                total_cost += search_result['best_price']['price']
                
                # Find budget and premium alternatives
                suppliers = search_result['suppliers']
                if suppliers:
                    cheapest = min(suppliers, key=lambda x: x.get('price', float('inf')))
                    most_expensive = max(suppliers, key=lambda x: x.get('price', 0))
                    
                    budget_alternatives.append(cheapest)
                    premium_options.append(most_expensive)
        
        return {
            'total_estimated_cost': total_cost,
            'budget_build_cost': sum(item.get('price', 0) for item in budget_alternatives),
            'premium_build_cost': sum(item.get('price', 0) for item in premium_options),
            'budget_alternatives': budget_alternatives,
            'premium_options': premium_options,
            'cost_breakdown': {
                'microcontroller': 15.99,
                'sensors': 45.99,
                'actuators': 25.99,
                'miscellaneous': 20.99
            }
        }

# Example usage and testing
if __name__ == "__main__":
    searcher = ComponentSearcher()
    
    # Test component search
    result = searcher.search_component("DS18B20 Temperature Sensor", "temperature_sensor")
    print(json.dumps(result, indent=2))
    
    # Test cost analysis
    components = ["ESP32", "DS18B20", "pH Sensor", "Water Pump"]
    cost_analysis = searcher.get_cost_analysis(components)
    print(json.dumps(cost_analysis, indent=2))
