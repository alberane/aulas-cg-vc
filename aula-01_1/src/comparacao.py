"""
Aula 1 - Comparação entre Computação Gráfica e Visão Computacional
Demonstração prática das diferenças entre OpenGL e OpenCV

Este programa mostra:
1. OpenGL: Síntese de uma imagem simples
2. OpenCV: Análise da imagem gerada
3. Matplotlib: Visualização dos resultados
"""

import time

import cv2
import matplotlib.pyplot as plt
import numpy as np


class ToolsComparison:
    def __init__(self):
        self.width = 400
        self.height = 400

    def create_synthetic_scene(self):
        """
        COMPUTAÇÃO GRÁFICA: Síntese de uma cena simples
        Cria uma imagem artificial com formas geométricas
        """
        print("=== COMPUTAÇÃO GRÁFICA: Síntese de Imagem ===")

        # Criar canvas vazio (fundo preto)
        image = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Adicionar formas geométricas usando OpenCV (simulando renderização)

        # 1. Retângulo azul
        cv2.rectangle(image, (50, 50), (150, 150), (255, 0, 0), -1)  # BGR: azul

        # 2. Círculo verde
        cv2.circle(image, (300, 100), 50, (0, 255, 0), -1)  # BGR: verde

        # 3. Triângulo vermelho
        triangle_points = np.array([[200, 200], [300, 350], [100, 350]], np.int32)
        cv2.fillPoly(image, [triangle_points], (0, 0, 255))  # BGR: vermelho

        # 4. Linha branca
        cv2.line(image, (0, 200), (400, 200), (255, 255, 255), 3)

        # 5. Texto
        cv2.putText(image, 'CG Scene', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        print("✓ Cena sintética criada com:")
        print("  - 1 retângulo azul")
        print("  - 1 círculo verde")
        print("  - 1 triângulo vermelho")
        print("  - 1 linha branca")
        print("  - Texto informativo")

        return image

    def analyze_scene(self, image):
        """
        VISÃO COMPUTACIONAL: Análise da imagem
        Extrai informações e características da imagem
        """
        print("\n=== VISÃO COMPUTACIONAL: Análise de Imagem ===")

        results = {}

        # 1. Converter para diferentes espaços de cor
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 2. Detecção de bordas
        edges = cv2.Canny(gray, 50, 150)

        # 3. Detecção de contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 4. Análise de cores dominantes
        pixels = image.reshape(-1, 3)
        non_black_pixels = pixels[np.any(pixels > [10, 10, 10], axis=1)]

        if len(non_black_pixels) > 0:
            unique_colors, counts = np.unique(non_black_pixels, axis=0, return_counts=True)
            dominant_colors = unique_colors[np.argsort(counts)[-3:]]  # Top 3 cores
        else:
            dominant_colors = []

        # 5. Detecção de formas usando aproximação de contornos
        shapes_detected = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filtrar contornos muito pequenos
                # Aproximar contorno
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Classificar forma baseado no número de vértices
                vertices = len(approx)
                if vertices == 3:
                    shapes_detected.append("Triângulo")
                elif vertices == 4:
                    shapes_detected.append("Retângulo")
                elif vertices > 8:
                    shapes_detected.append("Círculo")
                else:
                    shapes_detected.append(f"Polígono ({vertices} vértices)")

        # 6. Estatísticas da imagem
        results = {
            'dimensions': image.shape,
            'total_contours': len(contours),
            'shapes_detected': shapes_detected,
            'dominant_colors': dominant_colors,
            'edge_pixels': np.sum(edges > 0),
            'non_black_pixels': len(non_black_pixels),
            'brightness_mean': np.mean(gray),
            'brightness_std': np.std(gray)
        }

        # Imprimir resultados da análise
        print("✓ Análise completada:")
        print(f"  - Dimensões: {results['dimensions']}")
        print(f"  - Contornos detectados: {results['total_contours']}")
        print(f"  - Formas identificadas: {', '.join(results['shapes_detected'])}")
        print(f"  - Pixels de borda: {results['edge_pixels']}")
        print(f"  - Pixels não-pretos: {results['non_black_pixels']}")
        print(f"  - Brilho médio: {results['brightness_mean']:.1f}")
        print(f"  - Desvio padrão do brilho: {results['brightness_std']:.1f}")

        return results, gray, edges, hsv

    def create_visualization(self, original, gray, edges, hsv, results):
        """
        Criar visualização comparativa usando Matplotlib
        """
        print("\n=== VISUALIZAÇÃO: Comparação dos Resultados ===")

        # Configurar figura com subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Computação Gráfica vs Visão Computacional', fontsize=16, fontweight='bold')

        # 1. Imagem original (síntese CG)
        axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('SÍNTESE: Imagem Original\n(Computação Gráfica)', fontweight='bold')
        axes[0, 0].axis('off')

        # 2. Imagem em escala de cinza
        axes[0, 1].imshow(gray, cmap='gray')
        axes[0, 1].set_title('ANÁLISE: Escala de Cinza\n(Visão Computacional)', fontweight='bold')
        axes[0, 1].axis('off')

        # 3. Detecção de bordas
        axes[0, 2].imshow(edges, cmap='gray')
        axes[0, 2].set_title('ANÁLISE: Detecção de Bordas\n(Canny Edge Detection)', fontweight='bold')
        axes[0, 2].axis('off')

        # 4. Espaço de cor HSV
        axes[1, 0].imshow(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB))
        axes[1, 0].set_title('ANÁLISE: Espaço HSV\n(Hue-Saturation-Value)', fontweight='bold')
        axes[1, 0].axis('off')

        # 5. Histograma de intensidades
        axes[1, 1].hist(gray.flatten(), bins=50, color='gray', alpha=0.7)
        axes[1, 1].set_title('ANÁLISE: Histograma\n(Distribuição de Intensidades)', fontweight='bold')
        axes[1, 1].set_xlabel('Intensidade')
        axes[1, 1].set_ylabel('Frequência')
        axes[1, 1].grid(True, alpha=0.3)

        # 6. Cores dominantes
        if len(results['dominant_colors']) > 0:
            colors_normalized = results['dominant_colors'] / 255.0
            # Converter BGR para RGB para matplotlib
            colors_rgb = colors_normalized[:, [2, 1, 0]]  # Inverter BGR para RGB

            axes[1, 2].pie([1]*len(colors_rgb), colors=colors_rgb,
                          labels=[f'Cor {i+1}' for i in range(len(colors_rgb))],
                          autopct='%1.1f%%')
            axes[1, 2].set_title('ANÁLISE: Cores Dominantes\n(Palette Extraction)', fontweight='bold')
        else:
            axes[1, 2].text(0.5, 0.5, 'Nenhuma cor\ndominante detectada',
                           ha='center', va='center', transform=axes[1, 2].transAxes)
            axes[1, 2].set_title('ANÁLISE: Cores Dominantes\n(Palette Extraction)', fontweight='bold')

        plt.tight_layout()
        plt.show()

        print("Visualização criada com 6 painéis comparativos")

    def demonstrate_pipeline(self):
        """
        Demonstra o pipeline completo: Síntese → Análise → Visualização
        """
        print("DEMONSTRAÇÃO: Pipeline Computação Gráfica ↔ Visão Computacional")
        print("=" * 70)

        start_time = time.time()

        # Etapa 1: Síntese (Computação Gráfica)
        print("\n ETAPA 1: Síntese de Imagem")
        synthetic_image = self.create_synthetic_scene()

        # Etapa 2: Análise (Visão Computacional)
        print("\n🔍 ETAPA 2: Análise da Imagem")
        results, gray, edges, hsv = self.analyze_scene(synthetic_image)

        # Etapa 3: Visualização dos resultados
        print("\nETAPA 3: Visualização Comparativa")
        self.create_visualization(synthetic_image, gray, edges, hsv, results)

        total_time = time.time() - start_time
        print(f"\nPipeline executado em {total_time:.2f} segundos")

        # Salvar imagem original
        cv2.imwrite('synthetic_scene.png', synthetic_image)
        print(" Imagem salva como 'synthetic_scene.png'")

        return synthetic_image, results

    def interactive_demo(self):
        """
        Demonstração interativa com diferentes parâmetros
        """
        print("\n" + "="*50)
        print("DEMONSTRAÇÃO")
        print("="*50)

        # Parâmetros configuráveis
        configs = [
            {"name": "Cena Simples", "shapes": 3, "colors": 3},
            {"name": "Cena Complexa", "shapes": 5, "colors": 5},
            {"name": "Cena Monocromática", "shapes": 2, "colors": 1}
        ]

        for i, config in enumerate(configs):
            print(f"\n--- Configuração {i+1}: {config['name']} ---")

            # Criar cena com parâmetros específicos
            scene = self.create_synthetic_scene()

            # Análise rápida
            results, _, _, _ = self.analyze_scene(scene)

            print(f"Formas detectadas: {len(results['shapes_detected'])}")
            print(f"Complexidade (contornos): {results['total_contours']}")


def main():
    """Função principal da demonstração"""
    print("AULA 1 - INTRODUÇÃO À CG e VC")
    print("Demonstração: Computação Gráfica vs Visão Computacional")
    print("="*60)

    try:
        # Criar instância da demonstração
        demo = ToolsComparison()

        # Executar pipeline completo
        image, results = demo.demonstrate_pipeline()

        # Demonstração interativa adicional
        demo.interactive_demo()

        print("\n" + "="*60)
        print("RESUMO DA DEMONSTRAÇÃO:")
        print("Computação Gráfica: Criou uma cena sintética")
        print("Visão Computacional: Analisou e extraiu características")
        print("Visualização: Comparou os resultados lado a lado")
        print("\nCONCLUSÃO:")
        print(" CG e VC são áreas complementares")
        print(" CG: Modelo → Imagem (Síntese)")
        print(" VC: Imagem → Informação (Análise)")
        print(" Ambas usam matemática e algoritmos similares")
        print("="*60)

    except Exception as e:
        print(f"Erro durante execução: {e}")
        print("Verifique se todas as dependências estão instaladas:")
        print("pip install opencv-python matplotlib numpy")


if __name__ == "__main__":
    main()